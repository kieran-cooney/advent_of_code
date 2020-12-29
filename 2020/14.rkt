#lang racket

(define (read-mask line)
  (string->list (substring line 7)))

(define (get-int-from-regexp r s)
  (string->number (cadr (regexp-match r s))))

(define (read-mem-val line)
  (let* ([mem (get-int-from-regexp #px"\\[(\\d+)\\]" line)]
         [val (get-int-from-regexp #px"\\s(\\d+)$" line)])
    (cons mem val)))

(define (read-line line)
  (cond
    [(regexp-match-exact? #px"^mask.*" line) (read-mask line)]
    [(regexp-match-exact? #px"^mem.*" line) (read-mem-val line)]
    [else (raise-argument-error 'read-line "valid-input?" line)]))

(define (single-char-mask mask-char char)
  (if (equal? mask-char #\X) char mask-char))

(define (constant-list i x)
  (if (equal? i 0)
      null
      (cons x (constant-list (- i 1) x))))

(define (pad-lists mask-list bin-list)
  (let* ([len-mask-list (length mask-list)]
         [len-bin-list (length bin-list)]
         [len-list
          (if
           (> len-mask-list len-bin-list)
           len-mask-list
           len-bin-list)]
         [padded-mask-list
          (append (constant-list (- len-list len-mask-list) #\X) mask-list)]
         [padded-bin-list
          (append (constant-list (- len-list len-bin-list) #\0) bin-list)])
    (cons padded-mask-list padded-bin-list)))
         

(define (mask-integer mask i)
  (let* ([bin-string (number->string i 2)]
         [bin-cs (string->list bin-string)]
         [padded-lists (pad-lists mask bin-cs)]
         [padded-mask (car padded-lists)]
         [padded-bin-cs (cdr padded-lists)]
         [masked-cs (map single-char-mask padded-mask padded-bin-cs)]
         [masked-bin-string (list->string masked-cs)]
         [masked-i (string->number masked-bin-string 2)])
    masked-i))

(define (apply-bit-masks masks-and-vals)
  (letrec
      ([f
        (lambda (xs mask ht)
          (if (null? xs) ht
              (let* ([hd (first xs)]
                     [tl (rest xs)])
                (if (list? hd)
                    (f tl hd ht)
                    (let* ([mem-loc (car hd)]
                           [mem-val (cdr hd)]
                           [masked-val (mask-integer mask mem-val)]
                           [new-ht (hash-set ht mem-loc masked-val)])
                      (f tl mask new-ht))))))])
    (f (cdr masks-and-vals) (car masks-and-vals) (make-immutable-hash))))

(define (hash-sum ht)
  (apply + (hash-values ht)))

(displayln "Tests")
(define test-input (map read-line (file->lines "inputs/14_test.txt")))
(define test-mask (car test-input))
(for-each displayln test-input)
(displayln (apply-bit-masks test-input))
(displayln (hash-sum (apply-bit-masks test-input)))

(displayln "Answer for part 1")
(define input (map read-line (file->lines "inputs/14.txt")))
(displayln (hash-sum (apply-bit-masks input)))