#lang racket
(require racket/string)

(struct pol-pass (least-num most-num char password))

(define (count-char char cs count)
  (if (null? cs)
      count
      (let ([hd (car cs)] [tl (cdr cs)])
        (if (equal? char hd)
            (count-char char tl (+ count 1))
            (count-char char tl count)))))

(define (valid-password password)
  (let* ([char (pol-pass-char password)]
        [cs (string->list (pol-pass-password password))]
        [char-count (count-char char cs 0)]
        [least-num (pol-pass-least-num password)]
        [most-num (pol-pass-most-num password)])
    (if (and (<= char-count most-num) (>= char-count least-num))
        1
        0)))

(define (get-compare-char s i c)
  (if (>= i (string-length s))
      #f
      (equal? c (string-ref s i))))

(define (valid-password2 password)
    (let* ([char (pol-pass-char password)]
           [pw (pol-pass-password password)]
           [first-index (- (pol-pass-least-num password) 1)]
           [second-index (- (pol-pass-most-num password) 1)])
      (if (xor
           (get-compare-char pw first-index char)
           (get-compare-char pw second-index char))
          1
          0)))

(define (string->password s)
  (let* ([pol-pw-pair (string-split s ":")]
         [pw (string-trim (cadr pol-pw-pair))]
         [pol (car pol-pw-pair)]
         [limits-char-pair (string-split pol)]
         [limits (car limits-char-pair)]
         [char (string-ref (cadr limits-char-pair) 0)]
         [limit-pair (string-split limits "-")]
         [lower-limit (string->number (car limit-pair))]
         [upper-limit (string->number (cadr limit-pair))])
    (pol-pass lower-limit upper-limit char pw)))

(displayln
 (apply + (map valid-password
  (map string->password (file->lines "inputs/2.txt")))))

(displayln
 (apply + (map valid-password2
  (map string->password (file->lines "inputs/2.txt")))))