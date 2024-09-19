from urllib.parse import urljoin
from .adapter import LivetimingF1Request

def download_data(
    season_identifier: int,
    location_identifier: str = None,
    session_identifier: str | int = None
):
    last_data = None

    try:
        # Download season data
        season_data = LivetimingF1Request(urljoin(str(season_identifier) + "/", "Index.json"))
        last_data = season_data

        # Filter by location if provided
        if location_identifier:
            meeting_data = next(
                (meeting for meeting in season_data["Meetings"] if meeting["Location"] == location_identifier), 
                None
            )
            if meeting_data:
                last_data = meeting_data
            else:
                raise ValueError(f"Meeting with location '{location_identifier}' not found.")
        else:
            meeting_data = season_data["Meetings"]

        # Filter by session if provided
        if session_identifier:
            if isinstance(session_identifier, str):
                session_data = next(
                    (session for session in meeting_data['Sessions'] if session['Name'] == session_identifier), 
                    None
                )
            elif isinstance(session_identifier, int):
                session_data = next(
                    (session for session in meeting_data['Sessions'] if session['Key'] == session_identifier), 
                    None
                )
            
            if session_data:
                last_data = session_data
            else:
                raise ValueError(f"Session with identifier '{session_identifier}' not found.")
        
    except Exception as e:
        print(f"Error occurred: {e}")

    # Print and return the last data (filtered or entire dataset)
    return last_data