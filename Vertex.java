import java.util.ArrayList;
import java.util.List;

public class Vertex {

    String name;
    boolean visited;
    List<Vertex> negihbours = new ArrayList<>();

    public Vertex(String name) {
        this.name = name;
    }

    public List<Vertex> getNegihbours() {
        return negihbours;
    }

    public void addNegihbours(Vertex negihbour) {
        negihbours.add(negihbour);
    }

    public boolean isVisited() {
        return visited;
    }

    public void setVisited(boolean visited) {
        this.visited = visited;
    }
}
