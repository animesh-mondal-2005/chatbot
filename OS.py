import os
import requests
import math
import re

def clean_expression(raw):
    match = re.search(r"(math\.[a-z]+\([^\)]+\)|[\d\.\+\-\*/\(\)\s]+)", raw)
    return match.group(0) if match else ""

def perform_calculation(expression):
    try:
        expression = clean_expression(expression)
        result = eval(expression, {"__builtins__": None}, {"math": math})
        return f"The result of '{expression}' is {result}."
    except Exception as e:
        return f"Error in calculation: {str(e)}"

def is_valid_filename(filename):
    return bool(re.match(r'^[\w,\s-]+\.[A-Za-z]{1,5}$', filename))

def create_file(filename, content):
    if not is_valid_filename(filename):
        return f"Invalid filename: {filename}"
    try:
        with open(filename, 'w') as file:
            file.write(content)
        return f"File '{filename}' created successfully."
    except Exception as e:
        return f"Error creating file: {str(e)}"

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"File '{filename}' not found."
    except Exception as e:
        return f"Error reading file: {str(e)}"

def update_file(filename, content):
    try:
        with open(filename, 'a') as file:
            file.write(content)
        return f"Content appended to '{filename}' successfully."
    except FileNotFoundError:
        return f"File '{filename}' not found."
    except Exception as e:
        return f"Error updating file: {str(e)}"

def delete_file(filename):
    try:
        os.remove(filename)
        return f"File '{filename}' deleted successfully."
    except FileNotFoundError:
        return f"File '{filename}' not found."
    except Exception as e:
        return f"Error deleting file: {str(e)}"

def browse_internet(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        response = requests.get(url)
        response.raise_for_status()
        return response.text[:500] + "..."
    except requests.exceptions.RequestException as e:
        return f"Error accessing {url}: {str(e)}"

def parse_command(user_input):
    user_input = user_input.lower().strip()
    
    if user_input.startswith("create file"):
        try:
            parts = user_input.split("content:", 1)
            if len(parts) != 2:
                return "Please specify filename and content in format: create file filename.txt content: your content"
            filename = parts[0].split("filename:")[1].strip()
            content = parts[1].strip()
            return create_file(filename, content)
        except Exception as e:
            return f"Error processing create command: {str(e)}"
    
    elif user_input.startswith("read file"):
        try:
            filename = user_input.split("filename:")[1].strip()
            return read_file(filename)
        except Exception as e:
            return f"Error processing read command: {str(e)}"
    
    elif user_input.startswith("update file"):
        try:
            parts = user_input.split("content:", 1)
            if len(parts) != 2:
                return "Please specify filename and content in format: update file filename.txt content: your content"
            filename = parts[0].split("filename:")[1].strip()
            content = parts[1].strip()
            return update_file(filename, content)
        except Exception as e:
            return f"Error processing update command: {str(e)}"
    
    elif user_input.startswith("delete file"):
        try:
            filename = user_input.split("filename:")[1].strip()
            return delete_file(filename)
        except Exception as e:
            return f"Error processing delete command: {str(e)}"
    
    elif user_input.startswith("calculate"):
        try:
            expression = user_input.split("calculate", 1)[1].strip()
            return perform_calculation(expression)
        except Exception as e:
            return f"Error processing calculation: {str(e)}"
    
    elif user_input.startswith("browse"):
        try:
            url = user_input.split("url:")[1].strip()
            return browse_internet(url)
        except Exception as e:
            return f"Error processing browse command: {str(e)}"
    
    else:
        return "Available commands:\n" + \
               "- create file filename: filename.txt content: your content\n" + \
               "- read file filename: filename.txt\n" + \
               "- update file filename: filename.txt content: new content\n" + \
               "- delete file filename: filename.txt\n" + \
               "- calculate 2+2\n" + \
               "- browse url: example.com"

def main():
    print("Welcome to the File Management Chatbot!")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("Available commands: create file, read file, update file, delete file, calculate, browse")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break
            response = parse_command(user_input)
            print("Bot:", response)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print("Bot: An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    main()
