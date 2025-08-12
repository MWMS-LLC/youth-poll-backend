#!/usr/bin/env python3
"""
Youth Poll FastAPI Backend
==========================
Clean architecture with denormalized response storage
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
import os
from datetime import datetime
import uvicorn

# ======================
# Configuration
# ======================
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/youth_poll_pg')
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

# ======================
# Database Setup
# ======================
engine = create_engine(DATABASE_URL, echo=DEBUG)

# ======================
# Pydantic Models
# ======================
class VoteRequest(BaseModel):
    question_code: str
    option_code: str
    user_uuid: Optional[str] = None
    year_of_birth: Optional[int] = None

class OtherResponse(BaseModel):
    question_code: str
    other_text: str
    user_uuid: Optional[str] = None
    year_of_birth: Optional[int] = None

class CheckboxVoteRequest(BaseModel):
    question_code: str
    option_codes: List[str]  # Multiple options for checkbox questions
    other_text: Optional[str] = None  # Text for "OTHER" option
    user_uuid: Optional[str] = None
    year_of_birth: Optional[str] = None

# ======================
# FastAPI App
# ======================
app = FastAPI(
    title="Youth Poll API",
    description="Clean API for Youth Poll with denormalized response storage",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# Utility Functions
# ======================
def get_current_site(request: Request) -> str:
    """Get current site from request headers or default to 'youth'"""
    # Check for site header (for future multi-site support)
    site = request.headers.get('X-Site')
    if site:
        return site
    
    # Auto-detect site from Referer header
    referer = request.headers.get('Referer', '')
    if 'teen-poll-frontend' in referer:
        return 'teen'
    elif 'youth-poll-frontend' in referer:
        return 'youth'
    elif 'schools-poll-frontend' in referer:
        return 'schools'
    elif 'parents-poll-frontend' in referer:
        return 'parents'
    
    # Default to 'youth' if no referer or unknown
    return 'youth'

def get_question_data(question_code: str):
    """Get question and category data for denormalized storage"""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT q.question_code, q.question_text, q.question_number, q.block,
                   c.id as category_id, c.category_name, c.category_text
            FROM questions q
            JOIN categories c ON q.category_id = c.id
            WHERE q.question_code = :question_code
        """), {"question_code": question_code})
        
        row = result.fetchone()
        if row:
            return {
                "question_code": row[0],
                "question_text": row[1], 
                "question_number": row[2],
                "block_number": row[3],
                "category_id": row[4],
                "category_name": row[5],
                "category_text": row[6]
            }
        return None

def get_option_data(question_code: str, option_code: str):
    """Get option data for denormalized storage"""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, option_text, response_message, companion_advice
            FROM options
            WHERE question_code = :question_code AND option_code = :option_code
        """), {"question_code": question_code, "option_code": option_code})
        
        row = result.fetchone()
        if row:
            return {
                "option_id": row[0],
                "option_text": row[1],
                "response_message": row[2],
                "companion_advice": row[3]
            }
        return None

# ======================
# API Endpoints
# ======================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Youth Poll API is running", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

@app.get("/api/categories")
async def get_categories(request: Request):
    """Get all categories for current site"""
    try:
        site = get_current_site(request)
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, category_name, category_text, category_text_long, description
                FROM categories
                WHERE site = :site
                ORDER BY id
            """), {"site": site})
            
            categories = []
            for row in result:
                categories.append({
                    "id": row[0],
                    "category_name": row[1],
                    "category_text": row[2],
                    "text": row[2],  # Frontend expects 'text' field
                    "category_text_long": row[3],
                    "description": row[4]
                })
            
            return categories  # Return list directly, not wrapped in object
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/questions/{question_code}")
async def get_question(question_code: str):
    """Get a specific question with its options"""
    try:
        with engine.connect() as conn:
            # Get question details
            question_result = conn.execute(text("""
                SELECT q.question_code, q.question_text, q.question_number, q.block,
                       q.check_box, q.is_start_question,
                       c.id as category_id, c.category_name, c.category_text
                FROM questions q
                JOIN categories c ON q.category_id = c.id
                WHERE q.question_code = :question_code
            """), {"question_code": question_code})
            
            question_row = question_result.fetchone()
            if not question_row:
                raise HTTPException(status_code=404, detail="Question not found")
            
            # Get options
            options_result = conn.execute(text("""
                SELECT option_code, option_text, response_message, companion_advice, next_question_code
                FROM options
                WHERE question_code = :question_code
                ORDER BY option_code
            """), {"question_code": question_code})
            
            options = []
            for opt_row in options_result:
                options.append({
                    "option_code": opt_row[0],
                    "option_text": opt_row[1],
                    "response_message": opt_row[2],
                    "companion_advice": opt_row[3],
                    "next_question_code": opt_row[4]
                })
            
            return {
                "question": {
                    "question_code": question_row[0],
                    "question_text": question_row[1],
                    "question_number": question_row[2],
                    "block": question_row[3],
                    "check_box": question_row[4],
                    "is_start_question": question_row[5],
                    "category": {
                        "id": question_row[6],
                        "name": question_row[7],
                        "text": question_row[8]
                    }
                },
                "options": options
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/vote")
async def submit_vote(vote: VoteRequest, request: Request):
    """Submit a vote with denormalized storage"""
    try:
        site = get_current_site(request)
        
        # Generate user UUID if not provided
        if not vote.user_uuid:
            vote.user_uuid = str(uuid.uuid4())
        
        # Get question and option data for denormalized storage
        question_data = get_question_data(vote.question_code)
        if not question_data:
            raise HTTPException(status_code=404, detail="Question not found")
        
        option_data = get_option_data(vote.question_code, vote.option_code)
        if not option_data:
            raise HTTPException(status_code=404, detail="Option not found")
        
        # Store denormalized response
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO responses (
                    user_uuid, question_code, question_text, question_number,
                    category_id, category_name, category_text,
                    option_id, option_code, option_text, block_number,
                    setup_question_code, setup_option_id, site
                ) VALUES (
                    :user_uuid, :question_code, :question_text, :question_number,
                    :category_id, :category_name, :category_text,
                    :option_id, :option_code, :option_text, :block_number,
                    :setup_question_code, :setup_option_id, :site
                )
            """), {
                "user_uuid": vote.user_uuid,
                "question_code": question_data["question_code"],
                "question_text": question_data["question_text"],
                "question_number": question_data["question_number"],
                "category_id": question_data["category_id"],
                "category_name": question_data["category_name"],
                "category_text": question_data["category_text"],
                "option_id": option_data["option_id"],
                "option_code": vote.option_code,
                "option_text": option_data["option_text"],
                "block_number": question_data["block_number"],
                "setup_question_code": vote.question_code,
                "setup_option_id": option_data["option_id"],
                "site": site
            })
            conn.commit()
        
        return {
            "status": "success",
            "user_uuid": vote.user_uuid,
            "response_message": option_data.get("response_message"),
            "companion_advice": option_data.get("companion_advice")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting vote: {str(e)}")

@app.post("/api/other-response")
async def submit_other_response(response: OtherResponse, request: Request):
    """Submit free-text response with denormalized storage"""
    try:
        site = get_current_site(request)
        
        # Generate user UUID if not provided
        if not response.user_uuid:
            response.user_uuid = str(uuid.uuid4())
        
        # Get question data for denormalized storage
        question_data = get_question_data(response.question_code)
        if not question_data:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Store denormalized other response
        with engine.connect() as conn:
            # First, store the text response in other_responses
            conn.execute(text("""
                INSERT INTO other_responses (
                    user_uuid, other_text, question_code, question_text, question_number,
                    category_id, category_name, category_text, block_number,
                    setup_question_code, site
                ) VALUES (
                    :user_uuid, :other_text, :question_code, :question_text, :question_number,
                    :category_id, :category_name, :category_text, :block_number,
                    :setup_question_code, :site
                )
                ON CONFLICT (user_uuid, question_code) 
                DO UPDATE SET
                    other_text = EXCLUDED.other_text,
                    question_text = EXCLUDED.question_text,
                    question_number = EXCLUDED.question_number,
                    category_id = EXCLUDED.category_id,
                    category_name = EXCLUDED.category_name,
                    category_text = EXCLUDED.category_text,
                    block_number = EXCLUDED.block_number,
                    setup_question_code = EXCLUDED.setup_question_code,
                    site = EXCLUDED.site,
                    created_at = CURRENT_TIMESTAMP
            """), {
                "user_uuid": response.user_uuid,
                "other_text": response.other_text,
                "question_code": question_data["question_code"],
                "question_text": question_data["question_text"],
                "question_number": question_data["question_number"],
                "category_id": question_data["category_id"],
                "category_name": question_data["category_name"],
                "category_text": question_data["category_text"],
                "block_number": question_data["block_number"],
                "setup_question_code": response.question_code,
                "site": site
            })
            
            # Also create a vote record in responses table so it gets counted
            conn.execute(text("""
                INSERT INTO responses (
                    user_uuid, question_code, option_code, site
                ) VALUES (
                    :user_uuid, :question_code, :option_code, :site
                )
                ON CONFLICT (user_uuid, question_code) 
                DO UPDATE SET
                    option_code = EXCLUDED.option_code,
                    created_at = CURRENT_TIMESTAMP
            """), {
                "user_uuid": response.user_uuid,
                "question_code": question_data["question_code"],
                "option_code": "OTHER",  # This makes it count as a vote
                "site": site
            })
            
            conn.commit()
        
        return {
            "status": "success",
            "user_uuid": response.user_uuid
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting response: {str(e)}")

@app.get("/api/questions/{question_code}/results")
async def get_question_results_by_path(question_code: str, request: Request):
    """Get results for a specific question (frontend-compatible endpoint)"""
    return await get_question_results(question_code, request)

@app.get("/api/results/{question_code}")
async def get_question_results(question_code: str, request: Request):
    """Get results for a specific question"""
    try:
        site = get_current_site(request)
        with engine.connect() as conn:
            # Get standard responses with option text
            result = conn.execute(text("""
                SELECT r.option_code, 
                       CASE 
                           WHEN r.option_code = 'OTHER' THEN 'Other'
                           ELSE COALESCE(o.option_text, f'Option {r.option_code}')
                       END as option_text,
                       COUNT(*) as vote_count
                FROM responses r
                LEFT JOIN options o ON r.option_code = o.option_code AND r.question_code = o.question_code
                WHERE r.question_code = :question_code AND r.site = :site
                GROUP BY r.option_code, 
                         CASE 
                             WHEN r.option_code = 'OTHER' THEN 'Other'
                             ELSE COALESCE(o.option_text, f'Option {r.option_code}')
                         END
                ORDER BY r.option_code
            """), {"question_code": question_code, "site": site})
            
            # Get checkbox responses with option text
            checkbox_result = conn.execute(text("""
                SELECT cr.option_code, 
                       CASE 
                           WHEN cr.option_code = 'OTHER' THEN 'Other'
                           ELSE COALESCE(o.option_text, f'Option {cr.option_code}')
                       END as option_text,
                       COUNT(*) as vote_count
                FROM checkbox_responses cr
                LEFT JOIN options o ON cr.option_code = o.option_code AND cr.question_code = o.question_code
                WHERE cr.question_code = :question_code AND cr.site = :site
                GROUP BY cr.option_code, 
                         CASE 
                             WHEN cr.option_code = 'OTHER' THEN 'Other'
                             ELSE COALESCE(o.option_text, f'Option {cr.option_code}')
                         END
                ORDER BY cr.option_code
            """), {"question_code": question_code, "site": site})
            
            results = []
            total_votes = 0
            
            # Process standard responses
            for row in result:
                count = row[2]
                option_text = row[1] if row[1] else f"Option {row[0]}"  # Fallback if option_text is None
                total_votes += count
                results.append({
                    "option_code": row[0],
                    "option_text": option_text,
                    "vote_count": count
                })
            
            # Process checkbox responses
            for row in checkbox_result:
                count = row[2]
                option_text = row[1] if row[1] else f"Option {row[0]}"  # Fallback if option_text is None
                total_votes += count
                # Check if option already exists in results
                existing_option = next((r for r in results if r["option_code"] == row[0]), None)
                if existing_option:
                    existing_option["vote_count"] += count
                else:
                    results.append({
                        "option_code": row[0],
                        "option_text": option_text,
                        "vote_count": count
                    })
            
            # Calculate percentages
            for result_item in results:
                if total_votes > 0:
                    result_item["percentage"] = round((result_item["vote_count"] / total_votes) * 100, 1)
                else:
                    result_item["percentage"] = 0
            
            # Get other responses
            other_result = conn.execute(text("""
                SELECT other_text, created_at
                FROM other_responses
                WHERE question_code = :question_code AND site = :site
                ORDER BY created_at DESC
                LIMIT 50
            """), {"question_code": question_code, "site": site})
            
            other_responses = []
            for row in other_result:
                other_responses.append({
                    "text": row[0],
                    "submitted_at": row[1].isoformat() if row[1] else None
                })
            
            return {
                "question_code": question_code,
                "total_votes": total_votes,
                "results": results,
                "other_responses": other_responses
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting results: {str(e)}")

@app.get("/api/start-question/{category_id}")
async def get_start_question(category_id: int, request: Request):
    """Get the starting question for a category"""
    try:
        site = get_current_site(request)
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT question_code FROM questions 
                WHERE category_id = :category_id AND is_start_question = true 
                  AND site = :site
                ORDER BY question_number LIMIT 1
            """), {"category_id": category_id, "site": site})
            
            row = result.fetchone()
            if not row:
                # Fallback to first question in category
                result = conn.execute(text("""
                    SELECT question_code FROM questions 
                    WHERE category_id = :category_id AND site = :site
                    ORDER BY question_number LIMIT 1
                """), {"category_id": category_id, "site": site})
                row = result.fetchone()
                
            if not row:
                raise HTTPException(status_code=404, detail="No questions found for category")
                
            return {"question_id": row[0]}  # Frontend expects question_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/blocks/{category_id}")
async def get_blocks(category_id: int, request: Request):
    """Get all blocks for a category"""
    try:
        site = get_current_site(request)
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT b.block_number, b.block_text, b.category_name
                FROM blocks b
                WHERE b.category_id = :category_id AND b.site = :site
                ORDER BY b.block_number
            """), {"category_id": category_id, "site": site})
            
            blocks = []
            for row in result:
                block_text = row[1] or f"Block {row[0]}"
                
                # Check if block_text contains playlist link
                playlist_match = None
                if block_text and '[playlist:' in block_text:
                    import re
                    playlist_match = re.search(r'\[playlist:([a-zA-Z0-9_]+)\]', block_text)
                
                blocks.append({
                    "id": row[0],
                    "block_number": row[0],
                    "name": f"Block {row[0]}",
                    "description": block_text,
                    "playlist": playlist_match.group(1) if playlist_match else None
                })
            return blocks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/questions")
async def get_questions_by_category_block(category_id: int, block: int, request: Request):
    """Get questions for a specific category and block"""
    try:
        site = get_current_site(request)
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT q.question_code, q.question_text, q.question_number, q.block,
                       q.check_box, q.is_start_question,
                       c.id as category_id, c.category_name, c.category_text
                FROM questions q
                JOIN categories c ON q.category_id = c.id
                WHERE q.category_id = :category_id AND q.block = :block 
                  AND q.site = :site AND c.site = :site
                ORDER BY q.question_number
            """), {"category_id": category_id, "block": block, "site": site})
            
            questions = []
            for row in result:
                # Get options for this question
                options_result = conn.execute(text("""
                    SELECT option_code, option_text, next_question_code, 
                           response_message, companion_advice
                    FROM options 
                    WHERE question_code = :question_code
                    ORDER BY option_code
                """), {"question_code": row[0]})
                
                options = []
                for opt_row in options_result:
                    options.append({
                        "code": opt_row[0],
                        "text": opt_row[1],
                        "next_question_code": opt_row[2],
                        "response_message": opt_row[3],
                        "companion_advice": opt_row[4]
                    })
                
                questions.append({
                    "id": row[0],  # Use question_code as id for frontend compatibility
                    "question_code": row[0],
                    "question_text": row[1],
                    "question_number": row[2],
                    "block": row[3],
                    "check_box": bool(row[4]),
                    "is_start_question": bool(row[5]),
                    "category_id": row[6],
                    "category": {
                        "id": row[6],
                        "category_name": row[7],
                        "text": row[8]
                    },
                    "options": options
                })
            return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/next-question/{question_id}/{option_code}")
async def get_next_question(question_id: str, option_code: str):
    """Get next question based on current question and selected option"""
    try:
        with engine.connect() as conn:
            # Check if this option has a next_question_code
            result = conn.execute(text("""
                SELECT next_question_code FROM options
                WHERE question_code = ? AND option_code = ?
            """), (question_id, option_code))
            
            row = result.fetchone()
            if row and row[0]:
                # Return the specified next question
                return {"next_question_id": row[0]}
            else:
                # No specific next question - could implement logic to find next in sequence
                return {"next_question_id": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/checkbox-vote")
async def submit_checkbox_vote(vote: CheckboxVoteRequest, request: Request):
    """Submit checkbox vote with denormalized storage"""
    try:
        site = get_current_site(request)
        
        # Generate user UUID if not provided
        if not vote.user_uuid:
            vote.user_uuid = str(uuid.uuid4())
        
        # Get question data for denormalized storage
        question_data = get_question_data(vote.question_code)
        if not question_data:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Store each selected option as a separate response
        with engine.connect() as conn:
            for option_code in vote.option_codes:
                option_data = get_option_data(vote.question_code, option_code)
                if option_data:
                    conn.execute(text("""
                        INSERT INTO checkbox_responses (
                            user_uuid, question_code, question_text, question_number,
                            category_id, category_name, category_text,
                            option_id, option_code, option_text, block_number,
                            setup_question_code, setup_option_id, site
                        ) VALUES (
                            :user_uuid, :question_code, :question_text, :question_number,
                            :category_id, :category_name, :category_text,
                            :option_id, :option_code, :option_text, :block_number,
                            :setup_question_code, :setup_option_id, :site
                        )
                    """), {
                        "user_uuid": vote.user_uuid,
                        "question_code": question_data["question_code"],
                        "question_text": question_data["question_text"],
                        "question_number": question_data["question_number"],
                        "category_id": question_data["category_id"],
                        "category_name": question_data["category_name"],
                        "category_text": question_data["category_text"],
                        "option_id": option_data["option_id"],
                        "option_code": option_code,
                        "option_text": option_data["option_text"],
                        "block_number": question_data["block_number"],
                        "setup_question_code": vote.question_code,
                        "setup_option_id": option_data["option_id"],
                        "site": site
                    })
            
            # If OTHER is selected and other_text is provided, store it in other_responses
            if 'OTHER' in vote.option_codes and vote.other_text:
                # Store the OTHER option in checkbox_responses so it gets counted
                conn.execute(text("""
                    INSERT INTO checkbox_responses (
                        user_uuid, question_code, option_code, site
                    ) VALUES (
                        :user_uuid, :question_code, :option_code, :site
                    )
                """), {
                    "user_uuid": vote.user_uuid,
                    "question_code": question_data["question_code"],
                    "option_code": "OTHER",
                    "site": site
                })
                
                # Also store the text response in other_responses
                conn.execute(text("""
                    INSERT INTO other_responses (
                        user_uuid, question_code, question_text, question_number,
                        category_id, category_name, category_text, other_text,
                        block_number, setup_question_code, site
                    ) VALUES (
                        :user_uuid, :question_code, :question_text, :question_number,
                        :category_id, :category_name, :category_text, :other_text,
                        :block_number, :setup_question_code, :site
                    )
                    ON CONFLICT (user_uuid, question_code) 
                    DO UPDATE SET
                        other_text = EXCLUDED.other_text,
                        question_text = EXCLUDED.question_text,
                        question_number = EXCLUDED.question_number,
                        category_id = EXCLUDED.category_id,
                        category_name = EXCLUDED.category_name,
                        category_text = EXCLUDED.category_text,
                        block_number = EXCLUDED.block_number,
                        setup_question_code = EXCLUDED.setup_question_code,
                        site = EXCLUDED.site,
                        created_at = CURRENT_TIMESTAMP
                """), {
                    "user_uuid": vote.user_uuid,
                    "question_code": question_data["question_code"],
                    "question_text": question_data["question_text"],
                    "question_number": question_data["question_number"],
                    "category_id": question_data["category_id"],
                    "category_name": question_data["category_name"],
                    "category_text": question_data["category_text"],
                    "other_text": vote.other_text,
                    "block_number": question_data["block_number"],
                    "setup_question_code": vote.question_code,
                    "site": site
                })
            
            conn.commit()
        
        return {
            "status": "success",
            "user_uuid": vote.user_uuid,
            "selected_options": vote.option_codes
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting checkbox vote: {str(e)}")

@app.get("/api/stats")
async def get_stats():
    """Get overall poll statistics"""
    try:
        with engine.connect() as conn:
            # Total responses
            total_result = conn.execute(text("SELECT COUNT(*) FROM responses"))
            total_responses = total_result.scalar()
            
            # Total other responses
            other_result = conn.execute(text("SELECT COUNT(*) FROM other_responses"))
            total_other = other_result.scalar()
            
            # Unique users
            users_result = conn.execute(text("SELECT COUNT(DISTINCT user_uuid) FROM responses WHERE user_uuid IS NOT NULL"))
            unique_users = users_result.scalar()
            
            # Responses by category
            category_result = conn.execute(text("""
                SELECT category_name, COUNT(*) as count
                FROM responses
                GROUP BY category_name
                ORDER BY count DESC
            """))
            
            by_category = []
            for row in category_result:
                by_category.append({
                    "category": row[0],
                    "count": row[1]
                })
            
            return {
                "total_responses": total_responses,
                "total_other_responses": total_other,
                "unique_users": unique_users,
                "responses_by_category": by_category
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

# ======================
# Run the app
# ======================
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG
    )