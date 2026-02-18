"""
Custom initial messages for each encounter type.
These messages should feel like the actual person in the interaction.
"""

ENCOUNTER_INITIAL_MESSAGES = {
    # Airport encounters
    "Checking in at the Airport": "Good morning! Do you have your passport and flight information ready?",
    "Going Through Security": "Please place your carry-on items in the bin and remove your belt and shoes.",
    "Customs Declaration": "Welcome! Do you have anything to declare?",
    "Finding Your Gate": "Your gate is on the departure board. Do you need help finding it?",
    "Boarding the Plane": "We're now boarding. Please have your boarding pass ready.",
    "On the Plane": "Welcome aboard! Can I help you find your seat?",
    "Arriving at Destination": "Welcome! Please have your passport ready for immigration.",
    "Collecting Baggage": "Your baggage will arrive at carousel number 3. Do you need a cart?",
    "Leaving the Airport": "Do you need a taxi or transportation to your hotel?",
    
    # Banking encounters
    "Withdrawing Cash": "Good morning! How much would you like to withdraw today?",
    "Card Not Working": "I see there's an issue with your card. Let me check your account.",
    "Currency Exchange": "What currency would you like to exchange, and how much?",
    "Opening an Account": "Welcome! I'd be happy to help you open an account. Do you have your identification?",
    "ATM Not Dispensing": "I'm sorry about the ATM issue. Let me help you withdraw cash at the counter.",
    "Transfer Money": "Where would you like to transfer money to, and how much?",
    "Check Balance": "I can check your account balance. Do you have your account number?",
    "Report Lost Card": "I'm sorry to hear your card was lost. Let me help you report it.",
    
    # Clothing Shopping encounters
    "Finding Sizes": "Can I help you find your size? What are you looking for?",
    "Trying on Clothes": "The fitting rooms are over there. Would you like to try something on?",
    "Returning Items": "Do you have the receipt for this item?",
    "Asking for Help": "What can I help you find today?",
    "Price Check": "Let me check the price of that item for you.",
    "Payment Issues": "There seems to be an issue with your payment. Let me try again.",
    
    # Eating Out encounters
    "Ordering Coffee": "Good morning! What would you like to order?",
    "Reading the Menu": "Here's our menu. What looks good to you?",
    "Diet Restriction": "Do you have any allergies or dietary restrictions I should know about?",
    "Asking for the Bill": "Would you like anything else, or should I bring the check?",
    "Making a Reservation": "What time would you like to make a reservation for, and for how many people?",
    "Complaining about Food": "I'm sorry to hear that. What seems to be the problem?",
    
    # Groceries encounters
    "Shopping for Food": "Can I help you find anything today?",
    "Asking for Items": "What are you looking for? I can point you in the right direction.",
    "Checking Out": "Did you find everything you needed today?",
    "Price Question": "Let me check the price of that for you.",
    "Finding Products": "What product are you looking for? I can help you find it.",
    
    # Home Renovation encounters
    "Hiring a Contractor": "Good morning! What kind of work do you need done?",
    "Discussing Work": "Let me show you what we can do. What's your timeline?",
    "Getting a Quote": "I can give you an estimate. What exactly needs to be done?",
    "Scheduling Work": "When would be a good time to start the work?",
    "Payment for Work": "How would you like to pay for this work?",
    
    # Internet encounters
    "Setting up WiFi": "I can help you set up your WiFi. What's your address?",
    "Phone Plan": "What kind of phone plan are you looking for?",
    "No Service": "I'm sorry about the service issue. Let me check your account.",
    "Technician Visit": "The technician can come tomorrow. What time works for you?",
    "Billing Issue": "I see there's a problem with your bill. Let me look into it.",
    
    # Mechanic encounters
    "Car Won't Start": "What seems to be the problem with your car?",
    "Car Repairs": "I can take a look at your car. What's wrong with it?",
    "Getting an Estimate": "Let me check what needs to be fixed and give you an estimate.",
    "Scheduling Service": "When would you like to bring your car in?",
    "Paying for Repairs": "Your car is ready. How would you like to pay?",
    
    # Police Stop encounters
    "Traffic Stop": "Good afternoon. License and registration, please.",
    "Passport Check": "Can I see your passport and visa, please?",
    "Receiving a Fine": "You've received a traffic violation. Here's your ticket.",
    "Asking for Directions": "Can I help you with directions? Where are you trying to go?",
    
    # Small Talk encounters
    "Meeting Someone New": "Hello! Nice to meet you. What's your name?",
    "Asking How They Are": "How are you doing today?",
    "Responding to Greeting": "I'm doing well, thank you! How about you?",
    "Saying Goodbye": "It was nice talking to you! See you later.",
    "Making Small Talk": "How long have you been living here?",
}

def get_initial_message_for_encounter(encounter_title: str) -> str:
    """
    Get a custom initial message for an encounter based on its title.
    Falls back to a generic message if no specific message is found.
    """
    # Try to match the encounter title to our messages
    for key, message in ENCOUNTER_INITIAL_MESSAGES.items():
        if key in encounter_title:
            return message
    
    # Fallback to generic message
    return "Hello! How can I help you today?"



Custom initial messages for each encounter type.
These messages should feel like the actual person in the interaction.
"""

ENCOUNTER_INITIAL_MESSAGES = {
    # Airport encounters
    "Checking in at the Airport": "Good morning! Do you have your passport and flight information ready?",
    "Going Through Security": "Please place your carry-on items in the bin and remove your belt and shoes.",
    "Customs Declaration": "Welcome! Do you have anything to declare?",
    "Finding Your Gate": "Your gate is on the departure board. Do you need help finding it?",
    "Boarding the Plane": "We're now boarding. Please have your boarding pass ready.",
    "On the Plane": "Welcome aboard! Can I help you find your seat?",
    "Arriving at Destination": "Welcome! Please have your passport ready for immigration.",
    "Collecting Baggage": "Your baggage will arrive at carousel number 3. Do you need a cart?",
    "Leaving the Airport": "Do you need a taxi or transportation to your hotel?",
    
    # Banking encounters
    "Withdrawing Cash": "Good morning! How much would you like to withdraw today?",
    "Card Not Working": "I see there's an issue with your card. Let me check your account.",
    "Currency Exchange": "What currency would you like to exchange, and how much?",
    "Opening an Account": "Welcome! I'd be happy to help you open an account. Do you have your identification?",
    "ATM Not Dispensing": "I'm sorry about the ATM issue. Let me help you withdraw cash at the counter.",
    "Transfer Money": "Where would you like to transfer money to, and how much?",
    "Check Balance": "I can check your account balance. Do you have your account number?",
    "Report Lost Card": "I'm sorry to hear your card was lost. Let me help you report it.",
    
    # Clothing Shopping encounters
    "Finding Sizes": "Can I help you find your size? What are you looking for?",
    "Trying on Clothes": "The fitting rooms are over there. Would you like to try something on?",
    "Returning Items": "Do you have the receipt for this item?",
    "Asking for Help": "What can I help you find today?",
    "Price Check": "Let me check the price of that item for you.",
    "Payment Issues": "There seems to be an issue with your payment. Let me try again.",
    
    # Eating Out encounters
    "Ordering Coffee": "Good morning! What would you like to order?",
    "Reading the Menu": "Here's our menu. What looks good to you?",
    "Diet Restriction": "Do you have any allergies or dietary restrictions I should know about?",
    "Asking for the Bill": "Would you like anything else, or should I bring the check?",
    "Making a Reservation": "What time would you like to make a reservation for, and for how many people?",
    "Complaining about Food": "I'm sorry to hear that. What seems to be the problem?",
    
    # Groceries encounters
    "Shopping for Food": "Can I help you find anything today?",
    "Asking for Items": "What are you looking for? I can point you in the right direction.",
    "Checking Out": "Did you find everything you needed today?",
    "Price Question": "Let me check the price of that for you.",
    "Finding Products": "What product are you looking for? I can help you find it.",
    
    # Home Renovation encounters
    "Hiring a Contractor": "Good morning! What kind of work do you need done?",
    "Discussing Work": "Let me show you what we can do. What's your timeline?",
    "Getting a Quote": "I can give you an estimate. What exactly needs to be done?",
    "Scheduling Work": "When would be a good time to start the work?",
    "Payment for Work": "How would you like to pay for this work?",
    
    # Internet encounters
    "Setting up WiFi": "I can help you set up your WiFi. What's your address?",
    "Phone Plan": "What kind of phone plan are you looking for?",
    "No Service": "I'm sorry about the service issue. Let me check your account.",
    "Technician Visit": "The technician can come tomorrow. What time works for you?",
    "Billing Issue": "I see there's a problem with your bill. Let me look into it.",
    
    # Mechanic encounters
    "Car Won't Start": "What seems to be the problem with your car?",
    "Car Repairs": "I can take a look at your car. What's wrong with it?",
    "Getting an Estimate": "Let me check what needs to be fixed and give you an estimate.",
    "Scheduling Service": "When would you like to bring your car in?",
    "Paying for Repairs": "Your car is ready. How would you like to pay?",
    
    # Police Stop encounters
    "Traffic Stop": "Good afternoon. License and registration, please.",
    "Passport Check": "Can I see your passport and visa, please?",
    "Receiving a Fine": "You've received a traffic violation. Here's your ticket.",
    "Asking for Directions": "Can I help you with directions? Where are you trying to go?",
    
    # Small Talk encounters
    "Meeting Someone New": "Hello! Nice to meet you. What's your name?",
    "Asking How They Are": "How are you doing today?",
    "Responding to Greeting": "I'm doing well, thank you! How about you?",
    "Saying Goodbye": "It was nice talking to you! See you later.",
    "Making Small Talk": "How long have you been living here?",
}

def get_initial_message_for_encounter(encounter_title: str) -> str:
    """
    Get a custom initial message for an encounter based on its title.
    Falls back to a generic message if no specific message is found.
    """
    # Try to match the encounter title to our messages
    for key, message in ENCOUNTER_INITIAL_MESSAGES.items():
        if key in encounter_title:
            return message
    
    # Fallback to generic message
    return "Hello! How can I help you today?"



Custom initial messages for each encounter type.
These messages should feel like the actual person in the interaction.
"""

ENCOUNTER_INITIAL_MESSAGES = {
    # Airport encounters
    "Checking in at the Airport": "Good morning! Do you have your passport and flight information ready?",
    "Going Through Security": "Please place your carry-on items in the bin and remove your belt and shoes.",
    "Customs Declaration": "Welcome! Do you have anything to declare?",
    "Finding Your Gate": "Your gate is on the departure board. Do you need help finding it?",
    "Boarding the Plane": "We're now boarding. Please have your boarding pass ready.",
    "On the Plane": "Welcome aboard! Can I help you find your seat?",
    "Arriving at Destination": "Welcome! Please have your passport ready for immigration.",
    "Collecting Baggage": "Your baggage will arrive at carousel number 3. Do you need a cart?",
    "Leaving the Airport": "Do you need a taxi or transportation to your hotel?",
    
    # Banking encounters
    "Withdrawing Cash": "Good morning! How much would you like to withdraw today?",
    "Card Not Working": "I see there's an issue with your card. Let me check your account.",
    "Currency Exchange": "What currency would you like to exchange, and how much?",
    "Opening an Account": "Welcome! I'd be happy to help you open an account. Do you have your identification?",
    "ATM Not Dispensing": "I'm sorry about the ATM issue. Let me help you withdraw cash at the counter.",
    "Transfer Money": "Where would you like to transfer money to, and how much?",
    "Check Balance": "I can check your account balance. Do you have your account number?",
    "Report Lost Card": "I'm sorry to hear your card was lost. Let me help you report it.",
    
    # Clothing Shopping encounters
    "Finding Sizes": "Can I help you find your size? What are you looking for?",
    "Trying on Clothes": "The fitting rooms are over there. Would you like to try something on?",
    "Returning Items": "Do you have the receipt for this item?",
    "Asking for Help": "What can I help you find today?",
    "Price Check": "Let me check the price of that item for you.",
    "Payment Issues": "There seems to be an issue with your payment. Let me try again.",
    
    # Eating Out encounters
    "Ordering Coffee": "Good morning! What would you like to order?",
    "Reading the Menu": "Here's our menu. What looks good to you?",
    "Diet Restriction": "Do you have any allergies or dietary restrictions I should know about?",
    "Asking for the Bill": "Would you like anything else, or should I bring the check?",
    "Making a Reservation": "What time would you like to make a reservation for, and for how many people?",
    "Complaining about Food": "I'm sorry to hear that. What seems to be the problem?",
    
    # Groceries encounters
    "Shopping for Food": "Can I help you find anything today?",
    "Asking for Items": "What are you looking for? I can point you in the right direction.",
    "Checking Out": "Did you find everything you needed today?",
    "Price Question": "Let me check the price of that for you.",
    "Finding Products": "What product are you looking for? I can help you find it.",
    
    # Home Renovation encounters
    "Hiring a Contractor": "Good morning! What kind of work do you need done?",
    "Discussing Work": "Let me show you what we can do. What's your timeline?",
    "Getting a Quote": "I can give you an estimate. What exactly needs to be done?",
    "Scheduling Work": "When would be a good time to start the work?",
    "Payment for Work": "How would you like to pay for this work?",
    
    # Internet encounters
    "Setting up WiFi": "I can help you set up your WiFi. What's your address?",
    "Phone Plan": "What kind of phone plan are you looking for?",
    "No Service": "I'm sorry about the service issue. Let me check your account.",
    "Technician Visit": "The technician can come tomorrow. What time works for you?",
    "Billing Issue": "I see there's a problem with your bill. Let me look into it.",
    
    # Mechanic encounters
    "Car Won't Start": "What seems to be the problem with your car?",
    "Car Repairs": "I can take a look at your car. What's wrong with it?",
    "Getting an Estimate": "Let me check what needs to be fixed and give you an estimate.",
    "Scheduling Service": "When would you like to bring your car in?",
    "Paying for Repairs": "Your car is ready. How would you like to pay?",
    
    # Police Stop encounters
    "Traffic Stop": "Good afternoon. License and registration, please.",
    "Passport Check": "Can I see your passport and visa, please?",
    "Receiving a Fine": "You've received a traffic violation. Here's your ticket.",
    "Asking for Directions": "Can I help you with directions? Where are you trying to go?",
    
    # Small Talk encounters
    "Meeting Someone New": "Hello! Nice to meet you. What's your name?",
    "Asking How They Are": "How are you doing today?",
    "Responding to Greeting": "I'm doing well, thank you! How about you?",
    "Saying Goodbye": "It was nice talking to you! See you later.",
    "Making Small Talk": "How long have you been living here?",
}

def get_initial_message_for_encounter(encounter_title: str) -> str:
    """
    Get a custom initial message for an encounter based on its title.
    Falls back to a generic message if no specific message is found.
    """
    # Try to match the encounter title to our messages
    for key, message in ENCOUNTER_INITIAL_MESSAGES.items():
        if key in encounter_title:
            return message
    
    # Fallback to generic message
    return "Hello! How can I help you today?"



