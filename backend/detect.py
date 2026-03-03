import cv2

def classify_component(w, h):
    ratio = w / h
    area = w * h

    if area < 2500:
        return "checkbox"

    if ratio > 6:
        return "input"

    if 2 < ratio <= 6:
        return "button"

    if area > 40000:
        return "container"

    return "image"

def detect_ui_components(image_path, output_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)
    edges = cv2.Canny(blur, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    components = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        area = w * h

        if area > 1500 and w > 30 and h > 30:
            label = classify_component(w, h)

            components.append({
                "type": label,
                "x": int(x),
                "y": int(y),
                "w": int(w),
                "h": int(h)
            })

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            cv2.putText(img, label, (x, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    cv2.imwrite(output_path, img)
    return components