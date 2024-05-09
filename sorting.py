import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Data Sorting Visualization")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# Define sorting algorithms
sorting_algorithms = ["Bubble Sort", "Insertion Sort", "Merge Sort", "Quicksort", "Quantum Sort"]
current_algorithm_index = 0

# Define button dimensions
button_width = 150
button_height = 40
button_x = WINDOW_WIDTH - button_width - 20
button_y = 20

# Define font
font = pygame.font.Font(None, 24)

# Function to generate random data
def generate_data(size):
    return [random.randint(100, WINDOW_HEIGHT - 200) for _ in range(size)]

# Function to visualize the data
def visualize_data(data, algorithm_name, sorting=False):
    screen.fill(BLACK)

    # Calculate bar width and spacing
    bar_width = max(1, WINDOW_WIDTH // len(data) // 4)  # Decrease bar thickness
    spacing = bar_width // 2

    # Draw bars
    for i, value in enumerate(data):
        bar_x = i * (bar_width + spacing)
        bar_height = value
        if sorting:
            if algorithm_name == "Bubble Sort":
                color = RED
            elif algorithm_name == "Insertion Sort":
                color = GREEN
            elif algorithm_name == "Merge Sort":
                color = BLUE
            elif algorithm_name == "Quicksort":
                color = PURPLE
            elif algorithm_name == "Quantum Sort":
                color = YELLOW
        else:
            color = WHITE
        pygame.draw.rect(screen, color, (bar_x, WINDOW_HEIGHT - bar_height, bar_width, bar_height))

    # Display algorithm name
    text = font.render(algorithm_name, True, WHITE)
    screen.blit(text, (10, 10))

    # Draw buttons
    new_data_button = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, GRAY, new_data_button)
    new_data_text = font.render("New Data", True, BLACK)
    screen.blit(new_data_text, (new_data_button.x + 10, new_data_button.y + 10))

    algorithm_button = pygame.Rect(button_x, button_y + button_height + 10, button_width, button_height)
    pygame.draw.rect(screen, GRAY, algorithm_button)
    algorithm_text = font.render("Algorithm", True, BLACK)
    screen.blit(algorithm_text, (algorithm_button.x + 10, algorithm_button.y + 10))

    start_button = pygame.Rect(button_x, button_y + 2 * (button_height + 10), button_width, button_height)
    pygame.draw.rect(screen, GRAY, start_button)
    start_text = font.render("Start", True, BLACK)
    screen.blit(start_text, (start_button.x + 10, start_button.y + 10))

    stop_button = pygame.Rect(button_x, button_y + 3 * (button_height + 10), button_width, button_height)
    pygame.draw.rect(screen, GRAY, stop_button)
    stop_text = font.render("Stop", True, BLACK)
    screen.blit(stop_text, (stop_button.x + 10, stop_button.y + 10))

    exit_button = pygame.Rect(button_x, button_y + 4 * (button_height + 10), button_width, button_height)
    pygame.draw.rect(screen, GRAY, exit_button)
    exit_text = font.render("Exit", True, BLACK)
    screen.blit(exit_text, (exit_button.x + 10, exit_button.y + 10))

    # Draw dropdown menu
    dropdown_rect = pygame.Rect(algorithm_button.x, algorithm_button.y + algorithm_button.height, 200, button_height)
    pygame.draw.rect(screen, GRAY, dropdown_rect)
    dropdown_text = font.render(sorting_algorithms[current_algorithm_index], True, BLACK)
    screen.blit(dropdown_text, (dropdown_rect.x + 10, dropdown_rect.y + 10))

    # Draw data size input field
    input_rect = pygame.Rect(10, WINDOW_HEIGHT - 40, 200, 30)
    pygame.draw.rect(screen, GRAY, input_rect)
    input_text = font.render("Enter data size (min 10):", True, BLACK)
    screen.blit(input_text, (20, WINDOW_HEIGHT - 35))

    pygame.display.flip()

# Function to play audio during sorting
def play_audio(value1, value2, index, operation):
    if sorting_algorithms[current_algorithm_index] != "Quantum Sort":
        if operation == "compare":
            frequency = midi_to_frequency(60 + value1 - min(value1, value2))
        elif operation == "swap":
            frequency = midi_to_frequency(60 + value2 - min(value1, value2))
        sound = generate_tone(frequency, 0.1)
        sound.play()
        pygame.time.delay(50)  # Slow down sorting speed

# Function to generate a tone
def generate_tone(frequency, duration):
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    samples = [int(127 * (0.5 * math.sin(2 * math.pi * frequency * t / sample_rate))) for t in range(num_samples)]
    samples = [max(-127, min(127, sample)) for sample in samples]  # Clip samples to valid range
    bytes_samples = bytes(sample + 128 for sample in samples)  # Convert to unsigned bytes
    sound = pygame.mixer.Sound(buffer=bytes_samples)
    return sound

# Function to convert MIDI note number to frequency
def midi_to_frequency(note_number):
    return 440 * 2 ** ((note_number - 69) / 12)

# Define sorting algorithms
def bubble_sort(data):
    n = len(data)
    sorted_data = data.copy()
    stop_sorting = False
    while True:
        swapped = False
        for i in range(n - 1):
            play_audio(sorted_data[i], sorted_data[i + 1], i, "compare")
            if sorted_data[i] > sorted_data[i + 1]:
                play_audio(sorted_data[i], sorted_data[i + 1], i, "swap")
                sorted_data[i], sorted_data[i + 1] = sorted_data[i + 1], sorted_data[i]
                swapped = True
            visualize_data(sorted_data, sorting_algorithms[current_algorithm_index], sorting=True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    try:
                        pygame.quit()
                    except pygame.error:
                        pass
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if stop_button.collidepoint(pos) or exit_button.collidepoint(pos):
                        stop_sorting = True
                        break
            if stop_sorting:
                break
        if not swapped:
            break
    return sorted_data

def insertion_sort(data):
    sorted_data = data.copy()
    n = len(sorted_data)
    stop_sorting = False
    for i in range(1, n):
        key = sorted_data[i]
        j = i - 1
        while j >= 0 and key < sorted_data[j]:
            play_audio(key, sorted_data[j], j, "compare")
            sorted_data[j + 1] = sorted_data[j]
            j -= 1
            visualize_data(sorted_data, sorting_algorithms[current_algorithm_index], sorting=True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    try:
                        pygame.quit()
                    except pygame.error:
                        pass
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if stop_button.collidepoint(pos) or exit_button.collidepoint(pos):
                        stop_sorting = True
                        break
            if stop_sorting:
                break
        play_audio(key, sorted_data[j + 1], j + 1, "swap")
        sorted_data[j + 1] = key
    return sorted_data

def merge_sort(data):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left_half = merge_sort(data[:mid])
    right_half = merge_sort(data[mid:])

    sorted_data = []
    left_idx = right_idx = 0
    stop_sorting = False

    while left_idx < len(left_half) and right_idx < len(right_half):
        if left_half[left_idx] < right_half[right_idx]:
            play_audio(left_half[left_idx], right_half[right_idx], left_idx, "compare")
            sorted_data.append(left_half[left_idx])
            left_idx += 1
        else:
            play_audio(left_half[left_idx], right_half[right_idx], right_idx, "compare")
            sorted_data.append(right_half[right_idx])
            right_idx += 1

        visualize_data(sorted_data + left_half[left_idx:] + right_half[right_idx:], sorting_algorithms[current_algorithm_index], sorting=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    pygame.quit()
                except pygame.error:
                    pass
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if stop_button.collidepoint(pos) or exit_button.collidepoint(pos):
                    stop_sorting = True
                    break
        if stop_sorting:
            break

    sorted_data += left_half[left_idx:]
    sorted_data += right_half[right_idx:]

    return sorted_data

def quicksort(data):
    if len(data) <= 1:
        return data

    pivot = data[0]
    less_than_pivot = [x for x in data[1:] if x <= pivot]
    greater_than_pivot = [x for x in data[1:] if x > pivot]

    sorted_less_than_pivot = quicksort(less_than_pivot)
    sorted_greater_than_pivot = quicksort(greater_than_pivot)

    sorted_data = sorted_less_than_pivot + [pivot] + sorted_greater_than_pivot

    visualize_data(sorted_data, sorting_algorithms[current_algorithm_index], sorting=True)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            try:
                pygame.quit()
            except pygame.error:
                pass
            return
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if stop_button.collidepoint(pos) or exit_button.collidepoint(pos):
                return sorted_data

    return sorted_data

def quantum_sort(data):
    n = len(data)
    if n <= 1:
        return data

    # Create a list of indexes
    indexes = list(range(n))

    # Perform quantum operations on indexes
    stop_sorting = False
    for i in range(n):
        # Select a random pivot index
        pivot_index = random.randint(0, n - 1)

        # Partition the indexes based on the pivot
        less_than_pivot = [j for j in indexes if data[j] <= data[pivot_index]]
        greater_than_pivot = [j for j in indexes if data[j] > data[pivot_index]]

        # Update the indexes list
        indexes = less_than_pivot + [pivot_index] + greater_than_pivot

        # Visualize the sorting progress
        sorted_data = [data[j] for j in indexes]
        visualize_data(sorted_data, sorting_algorithms[current_algorithm_index], sorting=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    pygame.quit()
                except pygame.error:
                    pass
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if stop_button.collidepoint(pos) or exit_button.collidepoint(pos):
                    stop_sorting = True
                    break
        if stop_sorting:
            break

    # Sort the data based on the final indexes
    sorted_data = [data[j] for j in indexes]
    return sorted_data

def handle_button_click(pos, new_data_button, algorithm_button, start_button, stop_button, exit_button, dropdown_rect, input_rect, data_size):
    global data, current_algorithm_index, sorting, show_dropdown, exit_program
    if new_data_button.collidepoint(pos):
        data = generate_data(data_size)
        sorting = False
    elif algorithm_button.collidepoint(pos):
        show_dropdown = not show_dropdown
    elif start_button.collidepoint(pos):
        if not sorting:
            sorting = True
            if sorting_algorithms[current_algorithm_index] == "Bubble Sort":
                data = bubble_sort(data)
            elif sorting_algorithms[current_algorithm_index] == "Insertion Sort":
                data = insertion_sort(data)
            elif sorting_algorithms[current_algorithm_index] == "Merge Sort":
                data = merge_sort(data)
            elif sorting_algorithms[current_algorithm_index] == "Quicksort":
                data = quicksort(data)
            elif sorting_algorithms[current_algorithm_index] == "Quantum Sort":
                data = quantum_sort(data)
            sorting = False
    elif stop_button.collidepoint(pos):
        sorting = False
    elif exit_button.collidepoint(pos):
        exit_program = True
    elif dropdown_rect.collidepoint(pos):
        current_algorithm_index = (current_algorithm_index + 1) % len(sorting_algorithms)
        visualize_data(data, sorting_algorithms[current_algorithm_index], sorting)  # Update visualization
    elif input_rect.collidepoint(pos):
        data_size = get_data_size_input()
        if data_size is not None:
            data = generate_data(data_size)
    else:
        visualize_data(data, sorting_algorithms[current_algorithm_index], sorting)
def handle_data_size_input(event):
    global data_size_input
    if event.key == pygame.K_BACKSPACE:
        data_size_input = data_size_input[:-1]
    elif event.key == pygame.K_RETURN:
        data_size = get_data_size_input()
        if data_size is not None:
            data = generate_data(data_size)
    else:
        data_size_input += event.unicode
def get_data_size_input():
    global data_size_input
    data_size_input = ""
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    data_size_input = data_size_input[:-1]
                else:
                    data_size_input += event.unicode
    try:
        data_size = int(data_size_input)
        if data_size < 10:
            print("Data size should be at least 10. Using default value of 100.")
            data_size = 100
        return data_size
    except ValueError:
        print("Invalid input. Using default value of 100.")
        return 100

# Main loop
def main():
    global data, sorting, show_dropdown, data_size_input, exit_program

    data = generate_data(100)  # Generate initial data with 100 elements
    data_size_input = "100"
    sorting = False
    show_dropdown = False
    exit_program = False

    # Initialize buttons
    new_data_button = pygame.Rect(button_x, button_y, button_width, button_height)
    algorithm_button = pygame.Rect(button_x, button_y + button_height + 10, button_width, button_height)
    start_button = pygame.Rect(button_x, button_y + 2 * (button_height + 10), button_width, button_height)
    stop_button = pygame.Rect(button_x, button_y + 3 * (button_height + 10), button_width, button_height)
    exit_button = pygame.Rect(button_x, button_y + 4 * (button_height + 10), button_width, button_height)
    dropdown_rect = pygame.Rect(algorithm_button.x, algorithm_button.y + algorithm_button.height, 200, button_height)
    input_rect = pygame.Rect(10, WINDOW_HEIGHT - 40, 200, 30)

    while True:
        visualize_data(data, sorting_algorithms[current_algorithm_index], sorting)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or exit_program:
                try:
                    pygame.quit()
                except pygame.error:
                    pass
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                handle_button_click(pos, new_data_button, algorithm_button, start_button, stop_button, exit_button, dropdown_rect, input_rect, int(data_size_input))
                if exit_program:
                    try:
                        pygame.quit()
                    except pygame.error:
                        pass
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                handle_data_size_input(event)

if __name__ == "__main__":
    main()