from InquirerPy import inquirer
import subprocess

if __name__ == '__main__':

    file_path = 'ascii-art.txt'  

    with open(file_path, 'r', encoding='utf-8') as file:
        ascii_art = file.read()


    print(ascii_art)
    
    

    selected_option = inquirer.select(
        message="Choose an option:",
        choices=["I wanna play", "I wanna watch ai learning to play", ]
    ).execute()

    if selected_option == "I wanna play" :
        subprocess.run(["python", "game.py"])
    elif selected_option == "I wanna watch ai learning to play" :
        subprocess.run(["python", "ai-learning.py"])
        
