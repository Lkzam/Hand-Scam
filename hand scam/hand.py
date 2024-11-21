import cv2
import mediapipe as mp

# Inicializar MediaPipe Hand e desenhador
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Função para verificar se a mão está aberta ou fechada
def is_hand_open(hand_landmarks):
    tips_ids = [8, 12, 16, 20]  # Índices das pontas dos dedos (indicador, médio, anelar e mínimo)
    thumb_tip_id = 4  # Dedo polegar
    palm_bottom_id = 0  # Base da palma
    
    # Verificar se as pontas dos dedos estão acima das articulações mais próximas (aberto)
    fingers_up = []
    for tip_id in tips_ids:
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
            fingers_up.append(True)
        else:
            fingers_up.append(False)

    # Verificar o polegar (direção horizontal)
    if hand_landmarks.landmark[thumb_tip_id].x > hand_landmarks.landmark[thumb_tip_id - 1].x:
        fingers_up.append(True)
    else:
        fingers_up.append(False)

    return all(fingers_up)  # Retorna True se todos os dedos estiverem levantados

# Inicializar a câmera
cap = cv2.VideoCapture(0)

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar a imagem.")
            break
        
        # Converter para RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Detectar mãos
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Desenhar landmarks da mão
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Identificar se a mão está aberta ou fechada
                if is_hand_open(hand_landmarks):
                    cv2.putText(image, "Aberta", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(image, "Fechada", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Exibir a imagem com as informações
        cv2.imshow('Detecção de Mão', image)

        if cv2.waitKey(1) & 0xFF == 27:  # Pressione 'ESC' para sair
            break

cap.release()
cv2.destroyAllWindows()
