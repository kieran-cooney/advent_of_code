#lang racket

(define test-cases
  (list
   (cons (list 0 3 6) 436)
   (cons (list 1 3 2) 1)
   (cons (list 2 1 3) 10)
   (cons (list 1 2 3) 27)
   (cons (list 2 3 1) 78)
   (cons (list 3 2 1) 438)
   (cons (list 3 1 2) 1836)))

(define input (list 0 14 6 20 1 4))

(define (int-list i)
  (if (negative? i)
      null
      (cons i (int-list (- i 1)))))

(define (input->hash xs)
  (let* ([rev-xs (reverse xs)]
         [hd (car rev-xs)]
         [tl (cdr rev-xs)]
         [len-xs (length tl)]
         [pos-val-pairs (map cons tl (int-list (- len-xs 1)))]
         [ht (make-hash pos-val-pairs)])
    (list ht hd len-xs)))

(define (update-game-ht ht last-num num-numbers)
  (if (hash-has-key? ht last-num)
      (let* ([last-num-index (hash-ref ht last-num)]
             [last-num-age (- num-numbers last-num-index)])
        (begin (hash-set! ht last-num num-numbers)
               (list
                ht
                last-num-age
                (+ num-numbers 1))))
      (begin (hash-set! ht last-num num-numbers)
             (list
              ht
              0
              (+ num-numbers 1)))))

(define (get-ith-number ht last-num num-numbers i)
  (if (equal? i (add1 num-numbers))
      last-num
      (let* ([new-triple (update-game-ht ht last-num num-numbers)]
             [new-ht (car new-triple)]
             [new-last-num (cadr new-triple)]
             [new-num-numbers (caddr new-triple)])
        (get-ith-number new-ht new-last-num new-num-numbers i))))

(displayln "Tests")
(define first-test (caar test-cases))
(displayln first-test)
(define first-test-hash (input->hash first-test))
(displayln first-test-hash)
(define first-test-update
  (update-game-ht
   (car first-test-hash)
   (cadr first-test-hash)
   (caddr first-test-hash)))
(displayln first-test-update)
(displayln
 (get-ith-number
   (car first-test-hash)
   (cadr first-test-hash)
   (caddr first-test-hash)
   9))

(displayln "Answer for part 1")
(define ht-input (input->hash input))
(displayln
  (get-ith-number
   (car ht-input)
   (cadr ht-input)
   (caddr ht-input)
   2020))
(displayln "Answer for part 2")
(define ht-input-2 (input->hash input))
(displayln
  (get-ith-number
   (car ht-input-2)
   (cadr ht-input-2)
   (caddr ht-input-2)
   30000000))