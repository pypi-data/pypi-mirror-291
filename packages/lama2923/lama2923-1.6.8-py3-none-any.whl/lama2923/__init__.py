import os
import time
import socket
from colorama import Fore, Style, init
import requests
import sys
import datetime
import base64

if os.name == 'nt':
    import msvcrt
    

init()

def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        raise NotImplementedError("Unsupported Operating System!")

def calculate_elapsed_time(start_time, end_time):
    if not (isinstance(start_time, (int, float)) and isinstance(end_time, (int, float))):
        raise TypeError("Only time.time() or get_time() values are accepted!")

    time_difference = end_time - start_time
    seconds = int(time_difference)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    milliseconds = int((time_difference - int(time_difference)) * 1000)
    
    return {
        "Milliseconds": milliseconds,
        "Seconds": seconds if seconds > 0 else None,
        "Minutes": minutes if minutes > 0 else None,
        "Hours": hours if hours > 0 else None,
        "Days": days if days > 0 else None
    }

def get_time():
    return time.time()
    
def rainbow_text(TEXT, LOOP, Speed, section):
    def speed_control():
        if Speed not in ['Slow', 'Fast', None]:
            raise ValueError("Invalid speed value. Choose 'Slow', 'Fast', or None.")

    def section_control():
        if section not in ['Full', 'Half', 'Quarter', None]:
            raise ValueError("Invalid section value. Choose 'Full', 'Half', 'Quarter', or None.")

    speed_control()
    section_control()      
    
    init(autoreset=True)
    if not isinstance(LOOP, int):
        print("LOOP must be an integer!")
        time.sleep(3)
        clear_screen()
        exit(1)

    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

    text_length = len(TEXT)
    
    if section in ['Full', None]:
        section_count1 = 238
        section_count2 = section_count1 - 2
    elif section == 'Half':
        section_count1 = 119
        section_count2 = section_count1 - 2
    elif section == 'Quarter':
        section_count1 = 59
        section_count2 = section_count1 - 2 
               
    while True:
        if LOOP <= 0:
            break
        
        for i in range(1, section_count1 - text_length):
            for color in colors:
                if Speed in ['Slow']:
                    time.sleep(0.001)  
                elif Speed == 'Fast':
                    pass
                elif Speed is None:
                    time.sleep(0.0001)    
                print(" " * i + color + TEXT)

        for i in range(section_count2 - text_length, 0, -1):
            for color in colors:
                if Speed in ['Slow']:
                    time.sleep(0.001)  
                elif Speed == 'Fast':
                    pass
                elif Speed is None:
                    time.sleep(0.0001)   
                print(" " * i + color + TEXT)

def check_port(ip_address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip_address, port))
    sock.close()

    return result == 0

def check_internet():
    try:
        response = requests.get("http://www.google.com", timeout=2.5)
        return True
    except requests.ConnectionError:
        return False

def lprint(*text, end="\n", sep=" ", delay=0.10):
    text = map(str, text)
    combined_word = sep.join(text)
    word_len = len(combined_word)

    for char in combined_word:
        print(char, end="", flush=True)
        time.sleep(delay)

    print(end=end)

def clear_autocorrect():
    if os.name == 'nt':
        while msvcrt.kbhit():
            msvcrt.getch()

def linput(*text, end="", sep=" ", delay=0.10, autocorrect=False):
    lprint(*text, end=end, sep=sep, delay=delay)
    if autocorrect and os.name == 'nt':
        clear_autocorrect()
    return input()

def formatted_number(Numbers=0):
    if not isinstance(Numbers, (int, float, str)):
        raise TypeError("Value must be an integer, float, or a numeric string.")
    
    Numbers = str(float(Numbers)).replace('.', ',')
    integer_part, fractional_part = Numbers.split(',')

    formatted_integer_part = ".".join([
        integer_part[max(i - 3, 0):i]
        for i in range(len(integer_part), 0, -3)
    ][::-1])

    return f"{formatted_integer_part},{fractional_part}"

def reverse_formatted_number(Numbers=0):
    if not isinstance(Numbers, str):
        raise TypeError("Value must be a string.")
    return Numbers.replace(".", "").replace(",", ".")

def clear_autocorrect():
    if os.name == 'nt':
        while msvcrt.kbhit():
            msvcrt.getch()


def get_user_input(*prompts, sep=" ", end='\n', wend='', max_length=None, min_length=None,
                   force_int=False, allow_negative_int=False, force_str=False, require_input=False,
                   starts_with=("", False), required_starts=[], required_ends=[], 
                   choices=([], False), blocked_chars=r"", allowed_chars=r"",
                   required_input_len=0, auto_correct=False, input_color=None,
                   prompt_color=None, end_color=None, wend_color=None):
    
    # Join prompts with separator
    prompt_text = sep.join(map(str, prompts))
    
    # Validate mutually exclusive options
    mutually_exclusive = [force_str, force_int, allow_negative_int]
    if sum(mutually_exclusive) > 1:
        raise ValueError("force_str, force_int, and allow_negative_int cannot be used together.")
    
    # Clear autocorrect on Windows if required
    if os.name == "nt" and auto_correct:
        clear_autocorrect()

    selected_choice = False

    # Setup color mappings
    colors = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "black": Fore.BLACK,
    }
    
    # Initialize colors
    input_color = colors.get(input_color.lower(), "") if input_color else ""
    prompt_color = colors.get(prompt_color.lower(), "") if prompt_color else ""
    end_color = colors.get(end_color.lower(), "") if end_color else ""
    wend_color = colors.get(wend_color.lower(), "") if wend_color else ""
    
    # Function to update display
    def update_display():
        if any([prompt_color, input_color, wend_color, end_color]):
            sys.stdout.write(f'\r{prompt_color}{prompt_text}{Fore.RESET}{input_color}{input_str}{Fore.RESET}{wend_color}{wend}{Fore.RESET}' + ' ' * (len(end) + 1))
            sys.stdout.write(f'\r{prompt_color}{prompt_text}{Fore.RESET}{input_color}{input_str}{Fore.RESET}{wend_color}{wend}{Fore.RESET}')
            sys.stdout.write('\b' * len(wend))
            sys.stdout.flush()
        else:
            sys.stdout.write(f'\r{prompt_text}{input_str}{wend}' + ' ' * (len(end) + 1))
            sys.stdout.write(f'\r{prompt_text}{input_str}{wend}')
            sys.stdout.write('\b' * len(wend))
            sys.stdout.flush()

    # Function to get character input
    def getch():
        if os.name == "nt":
            import msvcrt
            return msvcrt.getwch()
        else:
            import termios
            import tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

    input_str = starts_with[0]
    update_display()

    while True:
        ch = getch()

        # Handle allowed and blocked characters
        if allowed_chars and ch not in allowed_chars and ch not in {'\r', '\n', "\b", "\x7f"}:
            continue
        
        if ch in blocked_chars:
            continue

        # Handle required start sequences
        if required_starts and ch not in {'\r', '\n', "\b", "\x7f"}:
            if not any(input_str.startswith(fs) or (len(input_str) < len(fs) and ch == fs[len(input_str)]) for fs in required_starts):
                continue

        # Handle Enter key
        if ch in {'\r', '\n'}:
            if choices[0]:
                valid_choice = False
                for choice in choices[0]:
                    if input_str == choice or (choices[1] and input_str.lower() == choice.lower()):
                        valid_choice = True
                        selected_choice = choice
                        break
                if not valid_choice:
                    continue

            if required_ends and not any(input_str.endswith(f) for f in required_ends):
                continue

            if require_input and not input_str:
                continue

            if required_input_len > 0 and len(input_str) != required_input_len:
                continue

            if min_length is not None and len(input_str) < min_length:
                continue
            
            break

        # Handle Backspace key
        elif ch in {'\b', '\x7f'}:
            if len(input_str) > 0:
                if starts_with[1] and len(input_str) == len(starts_with[0]):
                    pass
                else:
                    input_str = input_str[:-1]

        # Handle other input characters
        else:
            if max_length is None or len(input_str) < max_length:
                if force_int:
                    if ch.isdigit():
                        input_str += ch
                    elif allow_negative_int and ch == "-" and not input_str:
                        input_str += ch
                elif allow_negative_int and not force_str and (ch.isdigit() or (ch == "-" and not input_str)):
                    input_str += ch
                elif force_str:
                    try:
                        int(ch)
                    except ValueError:
                        input_str += ch
                else:
                    input_str += ch

        update_display()

    # Final display update
    sys.stdout.write(f'\r{prompt_color}{prompt_text}{Fore.RESET}{input_color}{input_str}{Fore.RESET}{wend_color}{wend}{Fore.RESET}{end_color}{end}{Fore.RESET}')
    sys.stdout.flush()

    return selected_choice if selected_choice else input_str




def get_directory_tree(startpath, depth=0, max_depth=float('inf'), prefix='', is_last=True, style='normal', custom_style=None, ingore_errors=False):
    if depth > max_depth:
        return ''
    
    tree_str = ''
    if depth == 0:
        tree_str += os.path.basename(startpath) + '\\\n'
    
    default_styles = {
        'normal': {'branch': ('├── ', '└── ', '|', '\\'), 'spacing': '    '},
        'bold': {'branch': ('┣━━ ', '┗━━ ', '┃', '\\'), 'spacing': '    '},
        'thin': {'branch': ('├─ ', '└─ ', '|', '\\'), 'spacing': '│  '},
        'compact': {'branch': ('', '', '|', '\\'), 'spacing': ''},
        'double': {'branch': ('╠══ ', '╚══ ', '║', '\\'), 'spacing': '    '},
        'dash': {'branch': ('|-- ', '`-- ', '|', '\\'), 'spacing': '    '},
        'star': {'branch': ('*-- ', '*-- ', '*', '\\'), 'spacing': '    '},
        'plus': {'branch': ('+-+ ', '+-+ ', '+', '\\'), 'spacing': '    '},
        'wave': {'branch': ('~-- ', '~-- ', '~', '\\'), 'spacing': '    '},
        'hash': {'branch': ('#-- ', '#-- ', '#', '\\'), 'spacing': '    '},
        'dot': {'branch': ('.-- ', '`-- ', '.', '\\'), 'spacing': '    '},
        'pipe': {'branch': ('|-- ', '|-- ', '|', '\\'), 'spacing': '    '},
        'slash': {'branch': ('/-- ', '/-- ', '/', '\\'), 'spacing': '    '},
        'backslash': {'branch': ('\\-- ', '\\-- ', '\\', '\\'), 'spacing': '    '},
        'equal': {'branch': ('=-- ', '=-- ', '=', '\\'), 'spacing': '    '},
        'colon': {'branch': (':-- ', ':-- ', ':', '\\'), 'spacing': '    '},
        'semicolon': {'branch': (';-- ', ';-- ', ';', '\\'), 'spacing': '    '},
        'exclamation': {'branch': ('!-- ', '!-- ', '!', '\\'), 'spacing': '    '},
        'question': {'branch': ('?-- ', '?-- ', '?', '\\'), 'spacing': '    '},
        'caret': {'branch': ('^-- ', '^-- ', '^', '\\'), 'spacing': '    '},
        'percent': {'branch': ('%-- ', '%-- ', '%', '\\'), 'spacing': '    '},
        'at': {'branch': ('@-- ', '@-- ', '@', '\\'), 'spacing': '    '},
        'tilde': {'branch': ('~-- ', '~-- ', '~', '\\'), 'spacing': '    '},
        'bracket': {'branch': ('[-- ', '[-- ', '[', '\\'), 'spacing': '    '},
        'brace': {'branch': ('{-- ', '{-- ', '{', '\\'), 'spacing': '    '},
        'paren': {'branch': ('(-- ', '(-- ', '(', '\\'), 'spacing': '    '},
        'angle': {'branch': ('<-- ', '<-- ', '<', '\\'), 'spacing': '    '},
        'quote': {'branch': ('"-- ', '"-- ', '"', '\\'), 'spacing': '    '},
        'apos': {'branch': ("'-- ", "'-- ", "'", '\\'), 'spacing': '    '},
        'underscore': {'branch': ('_-- ', '_-- ', '_', '\\'), 'spacing': '    '},
        'plusminus': {'branch': ('±-- ', '±-- ', '±', '\\'), 'spacing': '    '},
        'doubleangle': {'branch': ('«-- ', '«-- ', '«', '\\'), 'spacing': '    '},
        'box': {'branch': ('┏━ ', '┗━ ', '┃', '\\'), 'spacing': '    '},
        'arrow': {'branch': ('→-- ', '→-- ', '→', '\\'), 'spacing': '    '},
    }
    
    selected_style = custom_style if custom_style else default_styles.get(style, default_styles['normal'])
    
    spacing = selected_style['spacing']
    branch = selected_style['branch']
    
    if depth > 0:
        tree_str += prefix + (branch[1] if is_last else branch[0]) + os.path.basename(startpath) + branch[3] + '\n'
    
    prefix += spacing if is_last else branch[2] + spacing
    if ingore_errors:
        try:
            items = os.listdir(startpath)
            for i, item in enumerate(items):
                path = os.path.join(startpath, item)
                if os.path.isdir(path):
                    tree_str += get_directory_tree(path, depth + 1, max_depth, prefix, i == len(items) - 1, style, custom_style)
                else:
                    if style == 'box':
                        if i == len(items) - 1:
                            tree_str += prefix + branch[1] + item + '\n'
                        else:
                            tree_str += prefix + '┃━ ' + item + '\n'
                    else:
                        tree_str += prefix + (branch[1] if i == len(items) - 1 else branch[0]) + item + '\n'
        except:
            pass
    else:
        items = os.listdir(startpath)
        for i, item in enumerate(items):
            path = os.path.join(startpath, item)
            if os.path.isdir(path):
                tree_str += get_directory_tree(path, depth + 1, max_depth, prefix, i == len(items) - 1, style, custom_style)
            else:
                if style == 'box':
                    if i == len(items) - 1:
                        tree_str += prefix + branch[1] + item + '\n'
                    else:
                        tree_str += prefix + '┃━ ' + item + '\n'
                else:
                    tree_str += prefix + (branch[1] if i == len(items) - 1 else branch[0]) + item + '\n'
    
    
    return tree_str




class _Tools:
    def __init__(self):
        pass
    
    @staticmethod
    def control_file(file_name):
        return os.path.exists(file_name)
        

    
    @staticmethod
    def upload_image(image_path):
        try:
            url = "https://catbox.moe/user/api.php"
            payload = {
                'reqtype': 'fileupload'
            }
            files = {
                'fileToUpload': open(image_path, 'rb')
            }
            response = requests.post(url, data=payload, files=files)

            if response.status_code == 200:
                return response.text.strip()
            else:
                return None
        except:
            return None
        

    @staticmethod
    def url_check(url):
        try:
            response = requests.head(url, allow_redirects=True)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            return False
        
    @staticmethod
    def image_to_base64(image_path):
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
        

class TokenIsNotWork(Exception):
    pass

class Discord:
    
    class Embed:
        def __init__(self, title=None, description=None, color=0x3498db):
            self.embed = {
                "title": title,
                "description": description,
                "color": color,
                "fields": [],
                "author": {},
                "footer": {},
                "thumbnail": {},
                "image": {},
                "timestamp": None
            }

        def set_author(self, name, icon_url_or_path=None, url=None):
            icon_url = None
            if icon_url_or_path:
                if icon_url_or_path.startswith("http"):
                    if _Tools.url_check(icon_url_or_path):
                        icon_url = icon_url_or_path
                    else:
                        raise ValueError("URL is not valid.")
                else:
                    if _Tools.control_file(icon_url_or_path):
                        icon_url = _Tools.upload_image(icon_url_or_path)
                        if icon_url is None:
                            raise Exception("An issue occurred during the upload. Please try again using a URL instead of the file path.", icon_url_or_path)
                    else:
                        raise FileNotFoundError(f"File not found: {icon_url_or_path}")
                    
            self.embed["author"] = {"name": name, "icon_url": icon_url, "url": url}

        def add_field(self, name, value, inline=True):
            self.embed["fields"].append({"name": name, "value": value, "inline": inline})

        def set_footer(self, text, icon_url_or_path=None):
            icon_url = None
            if icon_url_or_path:
                if icon_url_or_path.startswith("http"):
                    if _Tools.url_check(icon_url_or_path):
                        icon_url = icon_url_or_path
                    else:
                        raise ValueError("URL is not valid.")
                else:
                    if _Tools.control_file(icon_url_or_path):
                        icon_url = _Tools.upload_image(icon_url_or_path)
                        if icon_url is None:
                            raise Exception("An issue occurred during the upload. Please try again using a URL instead of the file path.", icon_url_or_path)
                    else:
                        raise FileNotFoundError(f"File not found: {icon_url_or_path}")
                    
            self.embed["footer"] = {"text": text, "icon_url": icon_url}

        def set_thumbnail(self, url_or_path):
            url = None
            if url_or_path:
                if url_or_path.startswith("http"):
                    if _Tools.url_check(url_or_path):
                        url = url_or_path
                    else:
                        raise ValueError("URL is not valid.")
                else:
                    if _Tools.control_file(url_or_path):
                        url = _Tools.upload_image(url_or_path)
                        if url is None:
                            raise Exception("An issue occurred during the upload. Please try again using a URL instead of the file path.", url_or_path)
                    else:
                        raise FileNotFoundError(f"File not found: {url_or_path}")
                    
            self.embed["thumbnail"] = {"url": url}

        def set_image(self, url_or_path):
            url = None
            if url_or_path:
                if url_or_path.startswith("http"):
                    if _Tools.url_check(url_or_path):
                        url = url_or_path
                    else:
                        raise ValueError("URL is not valid.")
                else:
                    if _Tools.control_file(url_or_path):
                        url = _Tools.upload_image(url_or_path)
                        if url is None:
                            raise Exception("An issue occurred during the upload. Please try again using a URL instead of the file path.", url_or_path)
                    
                    else:
                        raise FileNotFoundError(f"File not found: {url_or_path}")
            else:
                raise ValueError("URL or path must be specified.")
            
            self.embed["image"] = {"url": url}

        def set_timestamp(self, timestamp=None):
            self.embed["timestamp"] = timestamp if timestamp else datetime.datetime.utcnow().isoformat()
            
        def to_dict(self):
            return self.embed
    
    class Author:
        def __init__(self, token):
            self.token = str(token)
            response = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': self.token})
            if response.status_code != 200:
                raise TokenIsNotWork('Token : \'{}\' is not working!'.format(self.token))
            
        def send_message(self, Channel_id, Message, files=None):
            not_files = []
            
            if files:
                for file in files:
                    if not _Tools.control_file(file):
                        not_files.append(file)
                        
            if not_files: 
                raise FileNotFoundError(f"Files not found: {', '.join(not_files)}")
        
            payload = {'content': str(Message)}
            headers = {'Authorization': self.token}


            if files is not None and isinstance(files, list):
                files_data = {}
                for file_name in files:
                    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
                        with open(file_name, "rb") as file:
                            files_data[os.path.basename(file_name)] = file.read()


                if files_data:
                    response = requests.post(f'https://discord.com/api/v9/channels/{Channel_id}/messages', data=payload, files=files_data, headers=headers)
                else:
                    response = requests.post(f'https://discord.com/api/v9/channels/{Channel_id}/messages', data=payload, headers=headers)
            else:
                response = requests.post(f'https://discord.com/api/v9/channels/{Channel_id}/messages', data=payload, headers=headers)

            return response.status_code

        def send_reply_message(self, channel_id, message, reply_message_id, files=None):
            not_files = []
            
            if files:
                not_files = [file for file in files if not _Tools.control_file(file)]
                            
            if not_files: 
                raise FileNotFoundError(f"Files not found: {', '.join(not_files)}")
            
            payload = {
                'content': str(message),
                'message_reference': {'message_id': reply_message_id}
            }
            headers = {'Authorization': self.token}
            
            if files and isinstance(files, list):
                files_data = {}
                for file_name in files:
                    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
                        with open(file_name, "rb") as file:
                            files_data[os.path.basename(file_name)] = file.read()
                
                if files_data:
                    response = requests.post(
                        f'https://discord.com/api/v9/channels/{channel_id}/messages',
                        data=payload,
                        files=files_data,
                        headers=headers
                    )
                else:
                    response = requests.post(
                        f'https://discord.com/api/v9/channels/{channel_id}/messages',
                        data=payload,
                        headers=headers
                    )
            else:
                response = requests.post(
                    f'https://discord.com/api/v9/channels/{channel_id}/messages',
                    data=payload,
                    headers=headers
                )
            
            return response.status_code
    
        def delete_message(self, Channel_id, Message_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/channels/{Channel_id}/messages/{Message_id}', headers=headers)
            return response.status_code
        
        def edit_message(self, Channel_id, Message_id, Message_Content):
            headers = {'Authorization': self.token}
            payload = {'content': str(Message_Content)}
            response = requests.patch(f'https://discord.com/api/v9/channels/{Channel_id}/messages/{Message_id}', json=payload, headers=headers)
            return response.status_code
        
        def get_channel_messages(self, channel_id, limit=50):
            headers = {'Authorization': self.token}
            all_messages = []
            last_message_id = None
    
            while len(all_messages) < limit:
                params = {'limit': min(50, limit - len(all_messages))}
                if last_message_id:
                    params['before'] = last_message_id
    
                response = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers, params=params)
                if response.status_code != 200:
                    try:
                        return response.status_code, response.json()
                    except:
                        return response.status_code, response.text
    
                messages = response.json()
                if not messages:
                    break
                
                all_messages.extend(messages)
                last_message_id = messages[-1]['id']
    
                if len(messages) < 50:
                    break
                
            return 200, all_messages
          
    
        def get_channel_message(self, Channel_id, Message_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/channels/{Channel_id}/messages/{Message_id}', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text

        def add_reaction(self, Channel_id, Message_id, emoji):
            headers = {'Authorization': self.token}
            emoji = requests.utils.quote(emoji)
            response = requests.put(f'https://discord.com/api/v9/channels/{Channel_id}/messages/{Message_id}/reactions/{emoji}/@me', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def remove_reaction(self, Channel_id, Message_id, emoji):
            headers = {'Authorization': self.token}
            emoji = requests.utils.quote(emoji)
            response = requests.delete(f'https://discord.com/api/v9/channels/{Channel_id}/messages/{Message_id}/reactions/{emoji}/@me', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text

        def get_channel_info(self, Channel_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/channels/{Channel_id}', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
    
        def get_guild_channels(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/guilds/{Guild_id}/channels', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text   

        def change_user_nickname(self, Guild_id, Nickname):
            headers = {'Authorization': self.token}
            payload = {'nick': str(Nickname)}
            response = requests.patch(f'https://discord.com/api/v9/guilds/{Guild_id}/members/@me/nick', json=payload, headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text

        def get_author_info(self):
            headers = {'Authorization': self.token}
            response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def get_author_relationships(self):
            headers = {'Authorization': self.token}
            response = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def send_friend_request(self, User_id):
            headers = {'Authorization': self.token}
            response = requests.put(f'https://discord.com/api/v9/users/@me/relationships/{User_id}', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def remove_friend(self, User_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/users/@me/relationships/{User_id}', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def block_user(self, User_id):
            headers = {'Authorization': self.token}
            response = requests.put(f'https://discord.com/api/v9/users/@me/relationships/{User_id}/block', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def unblock_user(self, User_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/users/@me/relationships/{User_id}/block', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text

        def get_author_channels(self):
            headers = {'Authorization': self.token}
            response = requests.get('https://discord.com/api/v9/users/@me/channels', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def get_author_guilds(self):
            headers = {'Authorization': self.token}
            response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def get_author_settings(self):
            headers = {'Authorization': self.token}
            response = requests.get('https://discord.com/api/v9/users/@me/settings', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
            
        def get_author_connections(self):
            headers = {'Authorization': self.token}
            response = requests.get('https://discord.com/api/v9/users/@me/connections', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def get_user_info(self, User_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/users/{User_id}', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text

        def get_all_guilds(self):
            headers = {'Authorization': self.token}
            response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def get_guild(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/guilds/{Guild_id}', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
            
        def kick_member(self, Guild_id, Member_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/guilds/{Guild_id}/members/{Member_id}', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def ban_member(self, Guild_id, Member_id, delete_message_days=0):
            headers = {'Authorization': self.token}
            data = {'delete_message_days': delete_message_days}
            response = requests.put(f'https://discord.com/api/v9/guilds/{Guild_id}/bans/{Member_id}', headers=headers, json=data)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def unban_member(self, Guild_id, Member_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/guilds/{Guild_id}/bans/{Member_id}', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def get_guild_bans(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/guilds/{Guild_id}/bans', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
            
        def get_guild_channels(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/guilds/{Guild_id}/channels', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def get_guild_members(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/guilds/{Guild_id}/members', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
            
        def get_guild_roles(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/guilds/{Guild_id}/roles', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
            
        def get_user_connections(self, id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/users/{id}/connections', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def join_channel(self, Channel_id):
            headers = {'Authorization': self.token}
            response = requests.put(f'https://discord.com/api/v9/channels/{Channel_id}/call/join', headers=headers)
            return response.status_code

        def leave_channel(self, Channel_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/channels/{Channel_id}/call', headers=headers)
            return response.status_code
        
        def delete_guild(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/guilds/{Guild_id}', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text

        def leave_guild(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/users/@me/guilds/{Guild_id}', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def get_webhooks(self, Channel_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/channels/{Channel_id}/webhooks', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text

        def create_webhook(self, Channel_id, Name, Avatar_path=None):
            headers = {'Authorization': self.token}
            data = {'name': Name}
            Avatar = None
            
            if _Tools.control_file(Avatar_path):
                encoded_avatar = _Tools.image_to_base64(Avatar_path)
                if encoded_avatar:
                    Avatar = encoded_avatar
                else:
                    raise Exception("An issue occurred during the upload. Please try again using a URL instead of the file path.", Avatar_path)
            else:
                raise FileNotFoundError(f"File not found: {Avatar_path}")
            
            if Avatar is not None:
                data['avatar'] = Avatar
                
            response = requests.post(f'https://discord.com/api/v9/channels/{Channel_id}/webhooks', headers=headers, json=data)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text

        def delete_webhook(self, webhook_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/webhooks/{webhook_id}', headers=headers)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text


        
    class Webhook:
        def __init__(self, webhook_url):
            self.WebhookUrl = str(webhook_url)
            
        def send_webhook(self, Content='', embeds=[], files=None):
            not_files = []
            
            if files:
                for file in files:
                    if not _Tools.control_file(file):
                        not_files.append(file)
                        
            if not_files: 
                raise FileNotFoundError(f"Files not found: {', '.join(not_files)}")
            
    
            data = {'content': Content}
            data['embeds'] = []
            if isinstance(embeds, list) or isinstance(embeds, tuple):
                for embed in embeds:
                    if embed:
                        if hasattr(embed, 'embed'):
                            data['embeds'].append(embed.embed)
                        else:
                            data['embeds'].append(embed)
            else:
                if embeds:
                    if hasattr(embeds, 'embed'):
                        data['embeds'].append(embeds.embed)
                    else:
                        data['embeds'].append(embeds)
            
            if files and isinstance(files, list):
                files_data = {os.path.basename(file_name): open(file_name, "rb").read() for file_name in files if os.path.getsize(file_name) > 0}
                response = requests.post(self.WebhookUrl, data=data, files=files_data)
            else:
                response = requests.post(self.WebhookUrl, json=data)
                
            return response.status_code
        
        
        def delete_message(self, Message_id):
            response = requests.delete(f'{self.WebhookUrl}/messages/{Message_id}')
            return response.status_code
        
        def get_message(self, Message_id):
            response = requests.get(f'{self.WebhookUrl}/messages/{Message_id}')
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
            
        def get_webhook_info(self):
            response = requests.get(self.WebhookUrl)
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
                
        def get_messages(self):
            response = requests.get(f'{self.WebhookUrl}/messages')
            try:
                return response.status_code, response.json()
            except:
                return response.status_code, response.text
        
        def edit_message(self, Message_id, Content='', embeds=[]):
            data = {'content': Content}
            data['embeds'] = []
            
            if isinstance(embeds, list) or isinstance(embeds, tuple):
                for embed in embeds:
                    if embed:
                        if hasattr(embed, 'embed'):
                            data['embeds'].append(embed.embed)
                        else:
                            data['embeds'].append(embed)
            else:
                if embeds:
                    if hasattr(embeds, 'embed'):
                        data['embeds'].append(embeds.embed)
                    else:
                        data['embeds'].append(embeds)
            
            response = requests.patch(f'{self.WebhookUrl}/messages/{Message_id}', json=data)
            return response.status_code



