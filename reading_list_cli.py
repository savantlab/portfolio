#!/usr/bin/env python3
"""
Reading List CLI - Command-line tool for managing reading list via API.

Usage:
    reading_list_cli.py auth <email>              # Get authentication token
    reading_list_cli.py verify <token>            # Verify token
    reading_list_cli.py add <title> [options]     # Add item to reading list
    reading_list_cli.py list                      # List all items
    reading_list_cli.py get <item_id>             # Get specific item
    reading_list_cli.py mark-read <item_id>       # Mark item as read
    reading_list_cli.py delete <item_id>          # Delete item

Environment Variables:
    API_URL          Base URL of the API (default: http://localhost:5001)
    API_TOKEN        Authentication token (or use 'reading_list_cli.py auth')
"""

import sys
import os
import json
import argparse
import requests
from urllib.parse import urljoin

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:5001")
API_TOKEN = os.getenv("API_TOKEN", None)


def make_request(method, endpoint, data=None, token=None):
    """Make authenticated API request."""
    url = urljoin(API_URL, endpoint)
    headers = {
        "Content-Type": "application/json"
    }
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            print(f"❌ Unknown method: {method}")
            return None
        
        if response.status_code >= 400:
            try:
                error_data = response.json()
                print(f"❌ Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"❌ Error {response.status_code}: {response.text}")
            return None
        
        return response.json()
    
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API at {API_URL}")
        print("   Make sure the Flask app is running: python flask_driver_runner.py app:app")
        return None
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None


def cmd_auth(args):
    """Request authentication token."""
    email = args.email
    
    print(f"Requesting token for {email}...")
    result = make_request("POST", "/api/auth/token", {"email": email})
    
    if result:
        token = result.get("token")
        print(f"✓ Token created: {token}")
        print(f"✓ Expires in: {result.get('expires_in')}")
        print(f"\nSave your token:")
        print(f"  export API_TOKEN=\"{token}\"")


def cmd_verify(args):
    """Verify and activate token."""
    token = args.token
    
    print("Verifying token...")
    result = make_request("POST", "/api/auth/verify", {"token": token})
    
    if result:
        print("✓ Token verified and activated!")


def cmd_add(args):
    """Add item to reading list."""
    if not API_TOKEN:
        print("❌ No API token set. Run: reading_list_cli.py auth <email>")
        sys.exit(1)
    
    data = {
        "title": args.title,
        "url": args.url,
        "description": args.description,
        "category": args.category
    }
    
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}
    
    print(f"Adding: {args.title}")
    result = make_request("POST", "/api/reading-list", data, API_TOKEN)
    
    if result:
        item_id = result.get("id")
        print(f"✓ Added item #{item_id}")
        print(f"  Title: {result.get('title')}")
        if result.get('url'):
            print(f"  URL: {result.get('url')}")
        print(f"  Category: {result.get('category')}")


def cmd_list(args):
    """List all reading list items."""
    if not API_TOKEN:
        print("❌ No API token set. Run: reading_list_cli.py auth <email>")
        sys.exit(1)
    
    result = make_request("GET", "/api/reading-list", token=API_TOKEN)
    
    if result is None:
        return
    
    if not result:
        print("📚 No items in reading list")
        return
    
    print(f"📚 Reading List ({len(result)} items)")
    print("=" * 70)
    
    for item in result:
        status = "✓" if item.get("completed") else " "
        print(f"\n[{status}] #{item['id']}: {item['title']}")
        if item.get("category"):
            print(f"    Category: {item['category']}")
        if item.get("description"):
            print(f"    {item['description']}")
        if item.get("url"):
            print(f"    URL: {item['url']}")


def cmd_get(args):
    """Get specific item."""
    if not API_TOKEN:
        print("❌ No API token set. Run: reading_list_cli.py auth <email>")
        sys.exit(1)
    
    result = make_request("GET", f"/api/reading-list/{args.item_id}", token=API_TOKEN)
    
    if result:
        print(f"Item #{result['id']}:")
        print(json.dumps(result, indent=2))


def cmd_mark_read(args):
    """Mark item as read."""
    if not API_TOKEN:
        print("❌ No API token set. Run: reading_list_cli.py auth <email>")
        sys.exit(1)
    
    result = make_request("POST", f"/api/reading-list/{args.item_id}/toggle", {}, API_TOKEN)
    
    if result:
        status = "marked as read" if result.get("completed") else "marked as unread"
        print(f"✓ Item #{args.item_id} {status}")


def cmd_delete(args):
    """Delete item."""
    if not API_TOKEN:
        print("❌ No API token set. Run: reading_list_cli.py auth <email>")
        sys.exit(1)
    
    if not args.force:
        confirm = input(f"Delete item #{args.item_id}? (y/n): ")
        if confirm.lower() != "y":
            print("Cancelled.")
            return
    
    result = make_request("DELETE", f"/api/reading-list/{args.item_id}", token=API_TOKEN)
    
    if result:
        print(f"✓ Item #{args.item_id} deleted")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Reading List CLI - Manage your reading list via API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get authentication token
  reading_list_cli.py auth stephaniea@savantlab.org

  # Verify token (after 2FA)
  reading_list_cli.py verify <token>

  # Add item
  reading_list_cli.py add "ML Papers" --url https://arxiv.org --category Research

  # List all items
  reading_list_cli.py list

  # Mark item as read
  reading_list_cli.py mark-read 1

  # Delete item
  reading_list_cli.py delete 1 --force
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Auth command
    auth_parser = subparsers.add_parser("auth", help="Request authentication token")
    auth_parser.add_argument("email", help="Your email address")
    auth_parser.set_defaults(func=cmd_auth)
    
    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify and activate token")
    verify_parser.add_argument("token", help="Authentication token to verify")
    verify_parser.set_defaults(func=cmd_verify)
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add item to reading list")
    add_parser.add_argument("title", help="Item title")
    add_parser.add_argument("--url", help="Item URL")
    add_parser.add_argument("--description", help="Item description")
    add_parser.add_argument("--category", help="Item category")
    add_parser.set_defaults(func=cmd_add)
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all items")
    list_parser.set_defaults(func=cmd_list)
    
    # Get command
    get_parser = subparsers.add_parser("get", help="Get specific item")
    get_parser.add_argument("item_id", type=int, help="Item ID")
    get_parser.set_defaults(func=cmd_get)
    
    # Mark read command
    read_parser = subparsers.add_parser("mark-read", help="Mark item as read/unread")
    read_parser.add_argument("item_id", type=int, help="Item ID")
    read_parser.set_defaults(func=cmd_mark_read)
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete item")
    delete_parser.add_argument("item_id", type=int, help="Item ID")
    delete_parser.add_argument("--force", action="store_true", help="Skip confirmation")
    delete_parser.set_defaults(func=cmd_delete)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
