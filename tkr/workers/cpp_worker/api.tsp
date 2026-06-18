@portmapping
model Ansatz {
    a: float;
    b: float;
    c: float;

}
interface TestNamespace {
  gen_inputs(value: string): Ansatz;
}
