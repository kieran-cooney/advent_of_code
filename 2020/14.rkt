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
         

(define (mask-integer-map single-char-mask-func mask i)
  (let* ([bin-string (number->string i 2)]
         [bin-cs (string->list bin-string)]
         [padded-lists (pad-lists mask bin-cs)]
         [padded-mask (car padded-lists)]
         [padded-bin-cs (cdr padded-lists)]
         [masked-cs (map single-char-mask-func padded-mask padded-bin-cs)])
    masked-cs))

(define (bin-list->number cs)
  (string->number (list->string cs) 2))

(define (single-char-mask mask-char char)
  (if (equal? mask-char #\X) char mask-char))

(define (single-char-mask-2 mask-char char)
  (if
   (equal? mask-char #\0)
   char
   mask-char))

(define (mask-integer mask i)
  (mask-integer-map single-char-mask mask i))

(define (mask-integer-2 mask i)
  (mask-integer-map single-char-mask-2 mask i))

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
                           [masked-val (bin-list->number (mask-integer mask mem-val))]
                           [new-ht (hash-set ht mem-loc masked-val)])
                      (f tl mask new-ht))))))])
    (f (cdr masks-and-vals) (car masks-and-vals) (make-immutable-hash))))

(define (prepend-to-list x)
  (lambda (l) (cons x l)))

(define (append-floating-char c xs)
  (if (equal? c #\X)
      (append
       (map (prepend-to-list #\0) xs)
       (map (prepend-to-list #\1) xs))
      (map (prepend-to-list c) xs)))

(define (expand-floating-bit-mask mask)
  (letrec
      ([f (lambda (cs xs)
            (if (null? cs)
                (map reverse xs)
                (let ([hd (car cs)]
                      [tl (cdr cs)])
                  (f tl (append-floating-char hd xs)))))])
    (f mask (list null))))

(define (expanded-hash-set ht keys val)
  (if (null? keys) ht
      (expanded-hash-set
       (hash-set ht (car keys) val)
       (cdr keys)
       val)))

(define (apply-bit-masks-2 masks-and-vals)
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
                           [masked-loc (mask-integer-2 mask mem-loc)]
                           [exp-mask-locs (expand-floating-bit-mask masked-loc)]
                           [new-ht (expanded-hash-set ht exp-mask-locs mem-val)])
                      (f tl mask new-ht))))))])
    (f (cdr masks-and-vals) (car masks-and-vals) (make-immutable-hash))))

(define (hash-sum ht)
  (apply + (hash-values ht)))

(displayln "Tests - part 1")
(define test-input (map read-line (file->lines "inputs/14_test.txt")))
(define test-mask (car test-input))
(for-each displayln test-input)
(displayln (apply-bit-masks test-input))
(displayln (hash-sum (apply-bit-masks test-input)))

(displayln "Answer for part 1")
(define input (map read-line (file->lines "inputs/14.txt")))
(displayln (hash-sum (apply-bit-masks input)))


(displayln "Tests - part 2")
(define test-input-2 (map read-line (file->lines "inputs/14_test2.txt")))
(for-each displayln test-input-2)
(define test-mask-2 (car test-input-2))
(displayln (hash-sum (apply-bit-masks-2 test-input-2)))

(displayln "Answer for part 2")
(displayln (hash-sum (apply-bit-masks-2 input)))