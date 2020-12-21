#lang racket

(define (clean-string s)
  (string-replace s " " ""))

(define (char-list->string cs)
  (string-join (map string cs) ""))

(define (remove-surrounding-brackets cs)
  (drop (take cs (- (length cs) 1)) 1))

(define (first-exp s)
  (letrec
      ([f (lambda (cs exp acc)
            (if (and (zero? acc) (not (null? exp)))
                (cons
                 (char-list->string (remove-surrounding-brackets exp))
                 (char-list->string cs))
                (let ([hd (car cs)]
                      [tl (cdr cs)])
                  (match hd
                    [#\( (f tl  (append exp (list hd)) (+ acc 1))]
                    [#\) (f tl  (append exp (list hd)) (- acc 1))]
                    [else (f tl  (append exp (list hd)) acc)]))))])
    (f (string->list s) (list) 0)))

(define (first-num s)
  (let* ([number-string (cadr (regexp-match #px"^(\\d+)(\\D|$)" s))]
         [number (string->number number-string)]
         [len-number (length (string->list number-string))]
         [tl (char-list->string (drop (string->list s) len-number))])
    (cons number tl)))
  
(define (first-item s)
  (let ([hd (string-ref s 0)])
    (if (equal? hd #\()
        (first-exp s)
        (first-num s))))

(define (operand? c)
  (or (equal? #\+) (equal? #\*)))

(define (string->exp-list s)
  (letrec
      ([first-split (first-item s)]
       [first-exp (cons #\+ (car first-split))]
       [first-exp-list (cons first-exp null)]
       [rest (cdr first-split)]
       [f
        (lambda (s1 exp-list)
          (if (equal? s1 "") exp-list
              (let* ([operand (string-ref s1 0)]
                     [body (substring s1 1)]
                     [split (first-item body)]
                     [new-s1 (cdr split)]
                     [new-exp-list (cons (cons operand (car split)) exp-list)])
                (f new-s1 new-exp-list))))])
    (f rest first-exp-list)))

(define (combine-exps e1 e2)
  (let* ([op-char (car e1)]
         [op (match op-char [#\+ +] [#\* *])]
         [result1 (eval-exp (cdr e1))]
         [result2 (eval-exp (cdr e2))])
    (cons null (op result1 result2))))

(define (eval-exp-list xs)
  (cdr (foldr combine-exps (cons null 0) xs)))

(define (eval-exp s)
  (cond
    [(number? s) s]
    [(regexp-match-exact? #px"^\\d+$" s) (string->number s)]
    [#t (eval-exp-list (string->exp-list s))]))

(displayln "Test cases")
(define test-cases (map clean-string (file->lines "inputs/18_test.txt")))
(map eval-exp test-cases)

(displayln "Answer for part 1")
(define expressions (map clean-string (file->lines "inputs/18.txt")))
(foldl + 0 (map eval-exp expressions))