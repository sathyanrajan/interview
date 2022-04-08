import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

public class Bsf {

    Vertex root;
    public Queue<Vertex> queue = new ConcurrentLinkedQueue<>();

    public Bsf(Vertex root) {
        this.root = root;
        queue.add(root);
    }

    public void traverse(){
        while(!queue.isEmpty()){
            Vertex currentVertex = queue.remove();
            if(!currentVertex.isVisited()){
                System.out.println("Visiting : " + currentVertex.name);
                currentVertex.setVisited(true);
            }
            for(Vertex iVertex : currentVertex.getNegihbours()){
                 queue.add(iVertex);
             }
        }
    }

}
