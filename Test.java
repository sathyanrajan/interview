public class Test {

    public static void main(String[] args) {
        Vertex a = new Vertex("A");
        Vertex b = new Vertex("B");
        Vertex c = new Vertex("C");
        Vertex d = new Vertex("D");
        Vertex e = new Vertex("E");
        Vertex f = new Vertex("F");

        a.addNegihbours(e);
        a.addNegihbours(f);
        f.addNegihbours(b);
        b.addNegihbours(c);
        b.addNegihbours(d);

        Bsf bsf = new Bsf(a);
        bsf.traverse();

    }
}
