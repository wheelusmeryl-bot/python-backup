def encrypt(text, num_rails):
    rails = [''] * num_rails
    direction_down = False
    current_rail = 0
    for char in text:
        rails[current_rail] += char
        if current_rail == 0 or current_rail == num_rails - 1:
            direction_down = not direction_down
        current_rail += 1 if direction_down else -1
    return ''.join(rails)
text = ""
num_rails = 3
encrypted_text = encrypt(text, num_rails)
print(f"Encrypted: {encrypted_text}")