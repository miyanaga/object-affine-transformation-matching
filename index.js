const cv = require("opencv4nodejs");

// 画像を読み込む
const imgA = cv.imread("a.jpg").bgrToGray();
const imgB = cv.imread("b.jpg").bgrToGray();

// 特徴量検出器の作成（例：ORB）
const orb = new cv.ORBDetector();

// 特徴点と記述子を検出
const keyPointsA = orb.detect(imgA);
const descriptorsA = orb.compute(imgA, keyPointsA);

const keyPointsB = orb.detect(imgB);
const descriptorsB = orb.compute(imgB, keyPointsB);

// 特徴点のマッチング（例：Brute-Force Matcher）
const bf = new cv.BFMatcher(cv.NORM_HAMMING, true);
const matches = bf.match(descriptorsA, descriptorsB);

// マッチング結果を距離でソート
matches.sort((a, b) => a.distance - b.distance);

// 上位のマッチを使用
const numMatches = 10;
const goodMatches = matches.slice(0, numMatches);

// 対応点を取得
const srcPoints = goodMatches.map((m) => keyPointsA[m.queryIdx].pt);
const dstPoints = goodMatches.map((m) => keyPointsB[m.trainIdx].pt);

// 変換行列を計算（例：アフィン変換）
const M = cv.estimateAffine2D(dstPoints, srcPoints);

console.log({ M });

// 画像Bを読み直して変換
const imgBColored = cv.imread("b.jpg");
const alignedImgB = imgBColored.warpAffine(
  M.out,
  new cv.Size(imgA.cols, imgA.rows)
);

cv.imwrite("aligned-b.jpg", alignedImgB);

console.log("done");
