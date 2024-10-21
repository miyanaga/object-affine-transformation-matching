# index.jsのPython類似バージョン
# 最後の数行は変更が必要です

import cv2
import numpy as np

# 画像を読み込む
imgA = cv2.imread('A.jpg', cv2.IMREAD_GRAYSCALE)
imgB = cv2.imread('B.jpg', cv2.IMREAD_GRAYSCALE)

# 特徴量検出器の作成（例：ORB）
orb = cv2.ORB_create()

# 特徴点と記述子を検出
kpA, desA = orb.detectAndCompute(imgA, None)
kpB, desB = orb.detectAndCompute(imgB, None)

# 特徴点のマッチング（例：Brute-Force Matcher）
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(desA, desB)

# マッチング結果を距離でソート
matches = sorted(matches, key=lambda x: x.distance)

# 上位のマッチを使用
num_matches = 10
good_matches = matches[:num_matches]

# 対応点を取得
src_pts = np.float32([kpA[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
dst_pts = np.float32([kpB[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)

# 変換行列を計算（例：アフィン変換）
M, mask = cv2.estimateAffine2D(dst_pts, src_pts)

# 画像Bを変換
rows, cols = imgA.shape
aligned_imgB = cv2.warpAffine(imgB, M, (cols, rows))

# 結果を表示または保存
cv2.imshow('Aligned Image', aligned_imgB)
cv2.waitKey(0)
cv2.destroyAllWindows()