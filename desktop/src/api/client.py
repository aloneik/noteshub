"""API Client for NoteHub Backend."""

import requests
from typing import Optional
from urllib.parse import urljoin

from logger import get_logger
from models import (
    User,
    Note,
    NoteWithPlans,
    Plan,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    NoteCreate,
    NoteUpdate,
    PlanCreate,
    PlanUpdate,
)

logger = get_logger(__name__)


class APIError(Exception):
    """Base exception for API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NoteHubClient:
    """Client for NoteHub FastAPI backend."""
    
    def __init__(self, base_url: str):
        """
        Initialize API client.
        
        Args:
            base_url: Backend URL (e.g., http://localhost:8000)
        """
        self.base_url = base_url.rstrip("/")
        self.token: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        logger.info(f"API Client initialized with base URL: {base_url}")
    
    def _get_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        return urljoin(self.base_url, endpoint)
    
    def _get_headers(self) -> dict:
        """Get headers with auth token if available."""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def _handle_response(self, response: requests.Response):
        """Handle HTTP response and raise errors if needed."""
        try:
            response.raise_for_status()
            logger.debug(f"Request successful: {response.request.method} {response.url} -> {response.status_code}")
        except requests.HTTPError as e:
            try:
                error_data = response.json()
                message = error_data.get("detail", str(e))
            except Exception:
                message = str(e)
            logger.error(f"API Error: {response.status_code} {message}")
            raise APIError(message, response.status_code)

    # Auth Methods

    def register(self, username: str, password: str) -> User:
        """
        Register a new user.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Created user
            
        Raises:
            APIError: If registration fails
        """
        logger.info(f"Registering user: {username}")
        url = self._get_url("/auth/register")
        data = RegisterRequest(username=username, password=password).model_dump()

        response = self.session.post(url, json=data)
        self._handle_response(response)

        user = User(**response.json())
        logger.info(f"User registered successfully: {user.username} (ID: {user.id})")
        return user

    def login(self, username: str, password: str) -> str:
        """
        Login and get access token.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Access token
            
        Raises:
            APIError: If login fails
        """
        url = self._get_url("/auth/login")
        # Login expects form data, not JSON
        data = {
            "username": username,
            "password": password,
        }
        
        response = self.session.post(
            url,
            data=data,  # Form data
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        self._handle_response(response)
        
        token_data = TokenResponse(**response.json())
        self.token = token_data.access_token
        return self.token
    
    def get_current_user(self) -> User:
        """
        Get current authenticated user info.
        
        Returns:
            Current user
            
        Raises:
            APIError: If not authenticated or request fails
        """
        url = self._get_url("/users/me")
        response = self.session.get(url, headers=self._get_headers())
        self._handle_response(response)
        
        return User(**response.json())
    
    # Notes Methods
    
    def get_notes(self) -> list[Note]:
        """
        Get all notes for current user.
        
        Returns:
            List of notes
            
        Raises:
            APIError: If request fails
        """
        url = self._get_url("/notes")
        response = self.session.get(url, headers=self._get_headers())
        self._handle_response(response)
        
        return [Note(**note) for note in response.json()]
    
    def get_note(self, note_id: int) -> NoteWithPlans:
        """
        Get a specific note with its plans.
        
        Args:
            note_id: Note ID
            
        Returns:
            Note with plans
            
        Raises:
            APIError: If note not found or request fails
        """
        url = self._get_url(f"/notes/{note_id}")
        response = self.session.get(url, headers=self._get_headers())
        self._handle_response(response)
        
        return NoteWithPlans(**response.json())
    
    def create_note(self, title: str, content: str = "") -> Note:
        """
        Create a new note.
        
        Args:
            title: Note title
            content: Note content (optional)
            
        Returns:
            Created note
            
        Raises:
            APIError: If creation fails
        """
        url = self._get_url("/notes")
        data = NoteCreate(title=title, content=content).model_dump()
        
        response = self.session.post(url, json=data, headers=self._get_headers())
        self._handle_response(response)
        
        return Note(**response.json())
    
    def update_note(
        self,
        note_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None
    ) -> Note:
        """
        Update a note.
        
        Args:
            note_id: Note ID
            title: New title (optional)
            content: New content (optional)
            
        Returns:
            Updated note
            
        Raises:
            APIError: If update fails
        """
        url = self._get_url(f"/notes/{note_id}")
        data = NoteUpdate(title=title, content=content).model_dump(exclude_none=True)
        
        response = self.session.put(url, json=data, headers=self._get_headers())
        self._handle_response(response)
        
        return Note(**response.json())
    
    def delete_note(self, note_id: int) -> None:
        """
        Delete a note.
        
        Args:
            note_id: Note ID
            
        Raises:
            APIError: If deletion fails
        """
        url = self._get_url(f"/notes/{note_id}")
        response = self.session.delete(url, headers=self._get_headers())
        self._handle_response(response)
    
    # Plans Methods
    
    def get_plans(self, note_id: int) -> list[Plan]:
        """
        Get all plans for a note.
        
        Args:
            note_id: Note ID
            
        Returns:
            List of plans
            
        Raises:
            APIError: If request fails
        """
        url = self._get_url(f"/notes/{note_id}/plans")
        response = self.session.get(url, headers=self._get_headers())
        self._handle_response(response)
        
        return [Plan(**plan) for plan in response.json()]
    
    def create_plan(
        self,
        note_id: int,
        title: str,
        is_done: bool = False
    ) -> Plan:
        """
        Create a new plan for a note.
        
        Args:
            note_id: Note ID
            title: Plan title
            is_done: Completion status (default: False)
            
        Returns:
            Created plan
            
        Raises:
            APIError: If creation fails
        """
        url = self._get_url(f"/notes/{note_id}/plans")
        data = PlanCreate(
            title=title,
            is_done=is_done
        ).model_dump()
        
        response = self.session.post(url, json=data, headers=self._get_headers())
        self._handle_response(response)
        
        return Plan(**response.json())
    
    def update_plan(
        self,
        note_id: int,
        plan_id: int,
        title: Optional[str] = None,
        is_done: Optional[bool] = None
    ) -> Plan:
        """
        Update a plan.
        
        Args:
            note_id: Note ID
            plan_id: Plan ID
            title: New title (optional)
            is_done: New completion status (optional)
            
        Returns:
            Updated plan
            
        Raises:
            APIError: If update fails
        """
        url = self._get_url(f"/notes/{note_id}/plans/{plan_id}")
        data = PlanUpdate(
            title=title,
            is_done=is_done
        ).model_dump(exclude_none=True)
        
        response = self.session.put(url, json=data, headers=self._get_headers())
        self._handle_response(response)
        
        return Plan(**response.json())
    
    def delete_plan(self, note_id: int, plan_id: int) -> None:
        """
        Delete a plan.
        
        Args:
            note_id: Note ID
            plan_id: Plan ID
            
        Raises:
            APIError: If deletion fails
        """
        url = self._get_url(f"/notes/{note_id}/plans/{plan_id}")
        response = self.session.delete(url, headers=self._get_headers())
        self._handle_response(response)
