import sys, os, io, subprocess, threading, socket, psutil, json, time, requests
import django
import webbrowser
from django.core.management import call_command

# **********************************************************************************************************************
def set_environment_variable(name, value):
    try:
        os.environ[name] = value
    except Exception as e:
        print(f"Error setting environment variable '{name}': {e}")

def set_environment_variable_persist(name, value):
    try:
        subprocess.run(['setx', name, value])
        # print(f"Environment variable '{name}' set to '{value}'")
    except Exception as e:
        # print(f"Error setting environment variable '{name}': {e}")
        pass

def find_process_by_port(port):
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

def is_port_available(port:int) -> bool:
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Try to connect to the specified port
            s.bind(("localhost", port))
            return True
    except socket.error:
        return False
    
def generate_port() -> int:
    port = 8664
    while not is_port_available(port):
        port += 1

    return port
# **********************************************************************************************************************

def set_spartaqube_shortcut():
    '''
    Set spartaqube exec to env
    '''
    current_path = os.path.dirname(__file__)
    base_path = os.path.dirname(current_path)
    spartaqube_exec = os.path.join(base_path, 'cli/spartaqube')
    set_environment_variable_persist('spartaqube', spartaqube_exec)

def db_make_migrations() -> bool:
    '''
    make migrations (DEPRECATED)
    '''
    current_path = os.path.dirname(__file__)
    base_path = os.path.dirname(current_path)
    process = subprocess.Popen("python manage.py makemigrations", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=base_path)
    stdout, stderr = process.communicate()
    
    if "No changes detected" in stdout.decode():
        return False # Do not need to apply migrate command
    
    if len(stderr) > 0:
        print(stderr.decode())
        return False

    return True

def db_migrate():
    '''
    migrate (DEPRECATED)
    '''
    current_path = os.path.dirname(__file__)
    base_path = os.path.dirname(current_path)
    process = subprocess.Popen("python manage.py migrate", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=base_path)
    stdout, stderr = process.communicate()
    if len(stderr) > 0:
        print(stderr.decode())

def db_make_migrations_migrate():
    '''
    
    '''
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    new_stdout, new_stderr = io.StringIO(), io.StringIO()
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = new_stdout, new_stderr
    try:
        call_command('makemigrations')
        call_command('migrate')
    finally:
        # Reset stdout and stderr to their original values    
        sys.stdout, sys.stderr = old_stdout, old_stderr
        
def create_public_user():
    '''
    Public user
    '''
    current_path = os.path.dirname(__file__)
    base_project = os.path.dirname(current_path)
    sys.path.insert(0, os.path.join(base_project, '/project/management'))
    from project.management.commands.createpublicuser import Command as CommandCreatePublicUser
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    CommandCreatePublicUser().handle()
    # current_path = os.path.dirname(__file__)
    # base_path = os.path.dirname(current_path)
    # process = subprocess.Popen("python manage.py createpublicuser", stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=base_path)
    # stdout, stderr = process.communicate()
    # print("stdout")
    # print(stdout)
    # if len(stderr) > 0:
    #     print(stderr.decode())

def create_admin_user():
    '''
    Admin user
    '''
    current_path = os.path.dirname(__file__)
    base_project = os.path.dirname(current_path)
    sys.path.insert(0, os.path.join(base_project, '/project/management'))
    from project.management.commands.createadminuser import Command as CommandCreateAdminUser
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    CommandCreateAdminUser().handle()
    # current_path = os.path.dirname(__file__)
    # base_path = os.path.dirname(current_path)
    # process = subprocess.Popen("python manage.py createadminuser", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=base_path)
    # stdout, stderr = process.communicate()
    # if len(stderr) > 0:
    #     print(stderr.decode())

def get_local_port():
    try:
        current_path = os.path.dirname(__file__)
        with open(os.path.join(current_path, 'app_data.json'), "r") as json_file:
            loaded_data_dict = json.load(json_file)
        
        return loaded_data_dict['port']
    except:
        return None

def is_application_running() -> bool:
    '''
    
    '''
    port = get_local_port()
    if port is None:
        return False
    else:
        if is_port_available(port):
            return False
        else:
            return True
        
def is_server_live(url):
    '''
    Ping the server to check if it's live
    '''
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False
    return False

def erase_line():
    sys.stdout.write('\r')
    sys.stdout.write(' ' * 80)
    sys.stdout.write('\r')
    sys.stdout.flush()

def start_server(port=None, b_print=True, b_open_browser=False):
    '''
    runserver at port
    '''

    if port is None:
        port = generate_port()
    else:
        if not is_port_available(port):
            # port = generate_port()
            raise Exception(f"{port} port is already used...")

    def thread_job():
        current_path = os.path.dirname(__file__)
        base_path = os.path.dirname(current_path)
        process = subprocess.Popen(f"python manage.py runserver 0.0.0.0:{port} &", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=base_path)
        stdout, stderr = process.communicate()
        if len(stderr) > 0:
            if b_print:
                print(stderr.decode())
        
    t = threading.Thread(target=thread_job, args=())
    t.start()
    
    i = 0
    while True:
        if b_print:
            # animation
            if i > 3:
                i = 0
            erase_line()
            sys.stdout.write(f'\rWaiting for server application{i*"."}')
            sys.stdout.flush()
            i += 1

        if is_server_live(f"http://127.0.0.1:{port}"):
            break
        time.sleep(1)  # Wait for a second before pinging again

    if b_print:
        erase_line()
        print(f"GUI exposed at http://localhost:{port}")
    
    app_data_dict = {'port': port}
    current_path = os.path.dirname(__file__)
    with open(os.path.join(current_path, "app_data.json"), "w") as json_file:
        json.dump(app_data_dict, json_file)

    if b_open_browser:
        webbrowser.open(f"http://localhost:{port}")

def stop_server(port=None):
    if port is None:
        port = get_local_port()

    if port is not None:
        process = find_process_by_port(port)
        if process:
            print(f"Found process running on port {port}: {process.pid}")
            process.terminate()
            print(f"SpartaQube server stopped")
        else:
            print(f"No process found running on port {port}.")
    else:
        raise Exception("Port not specify")

def django_setup():
    '''
    Set up Django environment
    '''
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spartaqube_app.settings')
    django.setup()

def entrypoint(port=None, force_startup=False, b_print=True, b_open_browser=False):
    '''
    
    '''
    if b_print:
        sys.stdout.write("Preparing SpartaQube, please wait...")
    
    if is_application_running() and not force_startup:
        if b_print:
            print(f"SpartaQube is running at http://localhost:{get_local_port()}")
    else:
        # set_spartaqube_shortcut()
        django_setup()
        # has_changes = db_make_migrations()
        # print("--- %s seconds db_make_migrations ---" % (time.time() - start_time))
        # if has_changes:
        #     db_migrate()
        db_make_migrations_migrate()
        create_public_user()
        create_admin_user()
        start_server(port=port, b_print=b_print, b_open_browser=b_open_browser)

    if b_print:
        print(f"SpartaQube documentation at http://localhost:{get_local_port()}/api")

if __name__ == '__main__':
    entrypoint()