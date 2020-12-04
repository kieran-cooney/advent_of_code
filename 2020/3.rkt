#lang racket
(require racket/string)

(define (count-trees forest i count step)
  (if (null? forest)
      count
      (let* ([hd (car forest)]
             [tl (cdr forest)]
             [width (string-length hd)]
             [loop-i (if (>= i width) (- i width) i)]
             [geog (string-ref hd loop-i)])
        (if (equal? #\# geog)
            (count-trees tl (+ loop-i step) (+ count 1) step)
            (count-trees tl (+ loop-i step) count step)))))

(define (count-trees-skip forest i count step)
  (if (or (null? forest) (null? (cdr forest)))
      count
      (let* ([hd (car forest)]
             [tl (cddr forest)]
             [width (string-length hd)]
             [loop-i (if (>= i width) (- i width) i)]
             [geog (string-ref hd loop-i)])
        (if (equal? #\# geog)
            (count-trees-skip tl (+ loop-i step) (+ count 1) step)
            (count-trees-skip tl (+ loop-i step) count step)))))


(displayln
 (count-trees (file->lines "inputs/3_test.txt") 0 0 1))
(displayln
 (count-trees (file->lines "inputs/3_test.txt") 0 0 3))
(displayln
 (count-trees (file->lines "inputs/3_test.txt") 0 0 5))
(displayln
 (count-trees (file->lines "inputs/3_test.txt") 0 0 7))
(displayln
 (count-trees-skip (file->lines "inputs/3_test.txt") 0 0 1))
(displayln
 (count-trees-skip (file->lines "inputs/3_test.txt") 0 0 0))

(displayln
 (count-trees (file->lines "inputs/3.txt") 0 0 3))

(displayln
 (apply * (list
      (count-trees (file->lines "inputs/3.txt") 0 0 1)
      (count-trees (file->lines "inputs/3.txt") 0 0 3)
      (count-trees (file->lines "inputs/3.txt") 0 0 5)
      (count-trees (file->lines "inputs/3.txt") 0 0 7)
      (count-trees-skip (file->lines "inputs/3.txt") 0 0 1))))