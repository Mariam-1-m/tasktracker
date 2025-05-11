from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.application import profile_service
from app.infrastructure.db.db  import get_db
from app.presentation.dependencies import get_current_user
from app.domain.models.user_model import AboutUpdateRequest
import os
from datetime import datetime

router = APIRouter(prefix="/profile", tags=["Profile"])

router = APIRouter()

@router.put("/update")
async def update_user_profile(
    name: str = Form(None),
    email: str = Form(None),
    phone: str = Form(None),
    photo: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    data = {}

    # Only update if the value is provided
    if name:
        data["username"] = name
    if email:
        data["email"] = email
    if phone:
        data["phone"] = phone

    # Handle photo upload (if provided)
    if photo:
        folder_path = "static/profile_photos"
        os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists

        filename = f"{current_user.id}_{photo.filename}"
        file_path = os.path.join(folder_path, filename)
        
        # Save photo to disk
        with open(file_path, "wb") as f:
            f.write(await photo.read())
        
        # Save the relative path to the database
        data["photo"] = f"profile_photos/{filename}"

    # Call your service layer to update the user in the database
    updated_user = profile_service.update_profile(db, current_user.id, data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Profile updated successfully"}


@router.post("/change-password")
def change_password(
    current_password: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not profile_service.change_password(db, current_user.id, current_password, new_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    return {"message": "Password updated"}

@router.delete("/delete")
def delete_account(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    success = profile_service.delete_user(db, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Account deleted"}

@router.get("/me")
def get_profile(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "photo": current_user.photo,
        "phone":current_user.phone,
        "job": current_user.job,
        "birthday": current_user.birthday,
        "location": current_user.location,
        "relation": current_user.relation,
        "education": current_user.education,
    }


@router.put("/about")
def update_about_route(
    birthday: str = Form(None),
    location: str = Form(None),
    relation: str = Form(None),
    job: str = Form(None),
    education: str = Form(None),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create a dictionary for data
    data = {}
    
    # Only add non-None fields
    if birthday:
        try:
            # Convert string to date
            data["birthday"] = datetime.strptime(birthday, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    if location:
        data["location"] = location
    if relation:
        data["relation"] = relation
    if job:
        data["job"] = job
    if education:
        data["education"] = education

    # Call the service to update the user
    updated_user = profile_service.update_about(db, user_id=current_user.id, data=data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "About info updated", "user_id": updated_user.id}