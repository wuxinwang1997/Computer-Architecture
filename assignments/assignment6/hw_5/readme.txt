Q:How to specify the sourse code file?
A:when calling the _initial_inst_queue() method in main function,just change the parameter:"source1.s"/"source.S"

Q:How to close the GUI?
A:at the last part of the main function,I use <tkinter> library to display the running process,just deleting them all is ok.


the configure of the reserved station is:
        Load/Store -->   2 clock
        Mul.D ---> 10 clock
        Div.D --> 40 clock
        Add.D/Sub.D  --> 2 clock
there is no extra latency for BNE/DADDUI


the drawbacks of this homework:
    1).since time is limited,so I don't encapsulate the displaying code in a class
    2).actually for the loop code,it's better to enroll them all firstly,but I didn't finish homework_3 very well,so this action would consume much more time.
