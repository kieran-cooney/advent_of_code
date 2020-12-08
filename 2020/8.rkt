#lang racket
(require racket/string)
(require racket/match)

(define (parse-instruction string)
  (let ([pr (string-split string " ")])
    (cons (car pr) (string->number (cadr pr)))))

(define (run-prog-one-line prog i acc)
  (let* ([pr (list-ref prog i)]
         [op (car pr)]
         [arg (cdr pr)])
    (match op
          ["acc" (cons (+ i 1) (+ acc arg))]
          ["jmp" (cons (+ i arg) acc)]
          ["nop" (cons (+ i 1) acc)])))

(define (find-loop-helper programme i acc states)
  (if (set-member? states i) acc
      (let* ([prog-pr (list-ref programme i)]
             [op (car prog-pr)]
             [arg (cdr prog-pr)]
             [new-states (set-add states i)]
             [out-pr (run-prog-one-line programme i acc)]
             [new-i (car out-pr)]
             [new-acc (cdr out-pr)])
        (find-loop-helper programme new-i new-acc new-states))))

(define (find-loop programme)
  (find-loop-helper programme 0 0 (set)))

; How to avoid nasty duplicating let expressions?
(define (valid-prog?-helper programme i acc states)
  (cond [(set-member? states i) (cons #f acc)]
        [(equal? i (length programme)) (cons #t acc)]
        [#t
         (let* ([prog-pr (list-ref programme i)]
                [op (car prog-pr)]
                [arg (cdr prog-pr)]
                [new-states (set-add states i)]
                [out-pr (run-prog-one-line programme i acc)]
                [new-i (car out-pr)]
                [new-acc (cdr out-pr)])
           (valid-prog?-helper programme new-i new-acc new-states))]))

(define (valid-prog? programme)
  (valid-prog?-helper programme 0 0 (set)))

(define (update-prog-pr prog-pr)
  (let ([op (car prog-pr)]
        [arg (cdr prog-pr)])
    (match op
      ["nop" (cons "jmp" arg)]
      ["jmp" (cons "nop" arg)])))


; I think there's a much better way to do this. Traverse the programme graph
; as usual, and keep a stack of (index, op, acc) everytime you cross "nop" or
; "jmp". When you loop back on yourself, return to the top element of the stack,
; swap and keep going. Continue to add to the stack as necessary. Note that you
; don't even need to be careful to make sure that you're preserving the new
; programme, as as soon as you have returned to a changed node, you have looped
; and so you go to the next element in the stack.
(define (find-valid-prog-helper programme i)
  (if (equal? i  (length programme))
      -1
      (let* ([prog-pr (list-ref programme i)]
             [op (car prog-pr)])
        (if (equal? op "acc") (find-valid-prog-helper programme (+ i 1))
            (let* ([new-prog (list-update programme i update-prog-pr)]
                   [valid-prog-pr (valid-prog? new-prog)]
                   [valid-prog (car valid-prog-pr)]
                   [acc (cdr valid-prog-pr)])
              (if valid-prog acc (find-valid-prog-helper programme (+ i 1))))))))

(define (find-valid-prog programme)
  (find-valid-prog-helper programme 0))

(displayln "Read in test")
(define test-programme
  (map parse-instruction (file->lines "inputs/8_test.txt")))
(for-each displayln test-programme)
(displayln "Accumulator at first loop for test")
(displayln (find-loop test-programme))
(displayln "Accumulator after fixing test programme")
(displayln (find-valid-prog test-programme))

(displayln "Accumulator at first loop (part 1)")
(define prog (map parse-instruction (file->lines "inputs/8.txt")))
(displayln (find-loop prog))
(displayln "Accumulator after fixing programme (part 2)")
(displayln (find-valid-prog prog))