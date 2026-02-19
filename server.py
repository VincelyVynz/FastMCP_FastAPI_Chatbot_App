from fastmcp import FastMCP
from db_utils import get_user_by_id, add_new_user, delete_user, get_all_users, delete_duplicate_users
from file_analysis_tools import read_text_file, read_xl_file

mcp = FastMCP("Database Operations with FastMCP and sqlite3")

@mcp.tool()
def get_user(user_id: int):
    """Get user info by id from database"""
    return get_user_by_id(user_id)

@mcp.tool()
def add_user(username: str, email: str, country: str):
    """Add a new user to the database"""
    add_new_user(username, email, country)

@mcp.tool()
def remove_user(user_id: int):
    """Remove a user from the database"""
    return delete_user(user_id)

@mcp.tool()
def list_all_users():
    """List all users in the database"""
    return get_all_users()

@mcp.tool()
def remove_duplicates():
    """Remove duplicate users from the database"""
    return delete_duplicate_users()

@mcp.tool()
def read_txt(filepath :str):
    """Read contents of a text file"""
    return read_text_file(filepath)

@mcp.tool()
def read_excel(filepath: str):
    """Read contents of an Excel file and return a pandas dictionary"""
    return read_xl_file(filepath)


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8080)