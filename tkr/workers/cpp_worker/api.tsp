@portmapping
model Ansatz {
    a: float;
    b: float;
    c: float;

}
interface cpp_worker {
  gen_inputs(value: string): Ansatz;
}
