import numpy as np
import cv2

# Video 
capture = cv2.VideoCapture('../videos/al.mkv')

# Returns the center of an object
def get_center(x, y, w, h):
    x1 = int(w/2)
    y1 = int(h/2)

    cx = x + x1
    cy = y + y1

    return cx, cy

candidates = [] # List of candidates to be a car

'''
    Inserts a car candidate to the list

    @args
        - width_threshold, height_threshold: limit to width/height increase/decrease between frames
        - center_threshold: limit to center movement between frames
        - count_threshold: times to act like a car to be a car
'''
def insertCandidate(newCandidate, width_threshold=0.2, height_threshold=0.2, 
                    center_threshold=50, count_threshold=20):
    global candidates

    # Look for corresponding object
    for candidate in candidates:
        # If width, height and center correspond, it is the same object
        if newCandidate['width'] > candidate['width'] * (1-width_threshold) and \
           newCandidate['width'] < candidate['width'] * (1+width_threshold) and \
           newCandidate['height'] > candidate['height'] * (1-height_threshold) and \
           newCandidate['height'] < candidate['height'] * (1+height_threshold) and \
           np.linalg.norm(np.array(newCandidate['center'])-np.array(candidate['center'])) < center_threshold:
            candidate['count'] += 1 # Object identified again
            candidate['width'], candidate['height'] = newCandidate['width'], newCandidate['height']
            candidate['center'], candidate['t'] = newCandidate['center'], newCandidate['t']

            # If it moves like a car, it is a car
            if not candidate['car'] and candidate['count'] > count_threshold:
                candidate['car'] = True

            return candidate
    
    # If it doesn't correspond to any existant object, it is a new one
    candidates.append(newCandidate)
    return newCandidate    

'''
    Removes old candidates, that probably are not cars

    @args
        - old_threshold: Amount of time unidentified before being desconsidered

'''
def removeOldCandidates(t, old_threshold=10):
    global candidates
    
    candidates_to_remove = []
    for candidate in candidates:
        # If it is an old object, removes it
        if candidate['t'] < t - old_threshold:
            candidates_to_remove.append(candidate)
    for candidate in candidates_to_remove:
        candidates.remove(candidate)

# Background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

t = 0   # Time
while True:
    ret, frame = capture.read() # Read frame

    # Change to gray
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    
    # Apply blur
    blur = cv2.GaussianBlur(grey, (7, 7), 15)   
    fgmask = fgbg.apply(blur)

    # Dilate
    dilated = cv2.dilate(fgmask, np.ones((5, 5)))

    # Apply kernel two times
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    dilated = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    # Find objects
    border, h = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Analyze objects
    for i, c in enumerate(border):
        x, y, w, h = cv2.boundingRect(c)

        # Minimum 60x60 size
        validate_border = (w >= 60) and (h >= 60)
        if not validate_border:
            continue

        # Get center
        center = get_center(x, y, w, h)

        # Create new candidate to be a car
        newCandidate = {
            'width': w,
            'height': h,
            'center': center,
            'count': 0,
            'car': False,
            't': t,
            # Random color
            'color': tuple(int(c) for c in np.random.choice(range(256), size=3))
        }
        
        # Insert candidate properly
        newCandidate = insertCandidate(newCandidate)

        # Draw candidate
        cv2.rectangle(frame, (x, y), (x+w, y+h), newCandidate['color'], 2)
        # If it is a car, center is green, otherwise is blue
        cv2.circle(frame, center, 4, (0, 255, 0) if newCandidate['car'] else (255, 0, 0), -1)

    # Remove old candidates
    removeOldCandidates(t)

    # Show frame
    cv2.imshow('frame', dilated)
    cv2.imshow('mask', frame)

    if cv2.waitKey(1) == 27:
        break
    
    t += 1

capture.release()
cv2.destroyAllWindows()