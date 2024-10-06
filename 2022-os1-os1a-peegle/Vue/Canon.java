package Vue;
import Modele.*;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.Point;
import java.awt.event.MouseEvent ;
import java.awt.image.BufferedImage;
import javax.swing.JPanel;



public class Canon extends JPanel{
    
    //pour le tracer la ligne de viser et eviter des calculs inutiles:
        int[] XLigneViser ;
        int[] YLigneViser ;
        
        double angleOrientation_old;
    
        private Ball balleATirer ;
    private BufferedImage image; 
    // Pointer à gauche revient à 0, à droite pi
    // en Radiant
    private double angleOrientation ;
    private Court court ;

    
    // parametre du canon :
    private double gravity = 100 ; 
    private int maxDistanceLigneTir ;
    private Point pivotDeRotation ;
    private static double vitesseTir = 450 ;
    private double tailleCanon = 6/100.0; // en pourcentage de la taille de l'écran
    private int angleMaxBord = 5 ;
    private int NbDeBallTirer = 0; 
    
    
    
    public int getNbDeBallTirer() {
        return NbDeBallTirer;
    }

    public Canon(Court court){ 

        
        
        // definition du Court
        this.court = court ;
        int largeurFrame = court.getWidth() ;
        setOpaque(false); //les balles ne passent plus derriere le jpanel du canon
        //background color black

        
        // Mise à l'echelle du canon :
        int tailleImage = (int) (largeurFrame* tailleCanon ) ;
        image = ImageImport.getImage("Gameview/cannonGrand.png", tailleImage, tailleImage) ;
        
        
        
        // position du canon initial à la vertical
        angleOrientation = Math.PI/2 ;     
        
        setBounds(largeurFrame/2 - image.getWidth()/2, getHeight()/4, image.getWidth(), image.getHeight());
        // tester si le canon est dans le court
        
        // definition point de pivot de rotation
        pivotDeRotation = new Point(getX() + getWidth()/2, getY() + getHeight()/2) ;
        

        // def max distance ligne tir :
            maxDistanceLigneTir = court.getHeight()/3 ;

            
        XLigneViser = new int[10];
        YLigneViser = new int[10];
    }
    
    public int[] getXLigneViser() {
        return XLigneViser;
    }

    public int[] getYLigneViser() {
        return YLigneViser;
    }
    


    public void setVitesseTir(double vitesseTir) {
        Canon.vitesseTir = vitesseTir;
    }


    public void setBalleATirer(Ball balleATirer) {
        this.balleATirer = balleATirer;
        gravity = balleATirer.getG();
        
        // Placement graphique :
        placementBallCanon();
        
    }

    public double getVitesseTir() {
        return Canon.vitesseTir;
    }
    
    private void placementBallCanon(){
        balleATirer.ballX = pivotDeRotation.x - Ball.ballRadius/2 - Math.cos(angleOrientation)*( this.getHeight()/2 );
        balleATirer.ballY = pivotDeRotation.y - Ball.ballRadius/2 + Math.sin(angleOrientation)*( this.getHeight()/2 ); 
    }

    public void deplacementCanon(boolean gauche){
        double deltaDeplacemnt  = 5 *(Math.PI/180) ;
        if (gauche) angleOrientation -= deltaDeplacemnt ;
        else angleOrientation += deltaDeplacemnt ;

        // Correction pour eviter des positions incongrue   
        if (angleOrientation >= (180-angleMaxBord)*(Math.PI/180) ) {
            angleOrientation = (180-angleMaxBord)*(Math.PI/180);
        }else if(angleOrientation < (angleMaxBord)*(Math.PI/180) ){
            angleOrientation = (angleMaxBord)*(Math.PI/180) ; 
        }
        

    }

    /**
     * @description Défini la vitesse de la balle pour amorcer le tir 
     *  place un nouvelle balle dans le lanceur
     * @author Thibault
     * @return Ball // ball qui vient d'être tirer
     */
    public Ball tirer(){
        // place la balle au bout du canon
        placementBallCanon();

        // definition de la vitesse de la balle
        balleATirer.ballSpeedX =  - vitesseTir*Math.cos(angleOrientation);
        balleATirer.ballSpeedY =  vitesseTir*Math.sin(angleOrientation);

        // creation d'une nouvelle ball
        Ball Ball_lancer = balleATirer ;
        balleATirer = new Ball(0, 0, 0, 0, court) ;

        // redéfinie la gravité pour chaque balle
        gravity = balleATirer.getG() ;

        NbDeBallTirer++ ;

        // return la balle tirer
        return Ball_lancer ;
    }

   
    /**
     * @author Thibault
     * @param Mouse Event
     * @description Permet de faire bouger le canon en fonction des coordonnées de la souris
     */
    public void DeplacementCanon(MouseEvent e){
        // calcul angle du canon 
        angleOrientation = Math.atan2((e.getY() - pivotDeRotation.y), (pivotDeRotation.x-e.getX()));

        // Correction pour eviter des positions incongrue
            if (angleOrientation >= (180-angleMaxBord)*(Math.PI/180) || angleOrientation < (angleMaxBord)*(Math.PI/180) ){
                if (e.getX()> pivotDeRotation.x) {
                    angleOrientation = (180-angleMaxBord)*(Math.PI/180);
                }else{
                    angleOrientation = (angleMaxBord)*(Math.PI/180) ; 
                }
            }
    }

    private double calculDeltaT(Point depart){
        double a = gravity*11*11 / 2.0; 
        double b = 11*vitesseTir*Math.sin(angleOrientation) ; 
        double delta = b*b - 4*a*(depart.y - maxDistanceLigneTir) ;

        return  (-b + Math.sqrt(delta))/(2*a) ; //racine du polynome
    } 
    

    public void calculCordonneeLigneViser(){
        Point depart = new Point((int)(pivotDeRotation.x + court.getInsets().left -  Math.cos(angleOrientation)*(this.getHeight()/2)), (int)(pivotDeRotation.y + Math.sin(angleOrientation)*(this.getHeight()/2) + court.getInsets().top )) ;
        
        //calcul du point d'arrivé de la ligne de visée

        double deltaT = calculDeltaT(depart) ; // adapte le deltaT pour que la ligne de viser s'adpate avec la taille maximun imposer
        if(angleOrientation != angleOrientation_old){
            for (int t = 1; t < 11; t++) {
                XLigneViser[t-1] = (int)(depart.x - deltaT*t * vitesseTir * Math.cos(angleOrientation));
                YLigneViser[t-1] = (int)(depart.y + deltaT *t* vitesseTir * Math.sin(angleOrientation) + gravity*deltaT * deltaT*t*t  / 2.0);
            }
        }
        angleOrientation_old = angleOrientation;
    }

    
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2D = (Graphics2D) g ;
        
        // orientation du canon :
        
        g2D.rotate( Math.PI/2- angleOrientation, getWidth()/2, getHeight()/2);
        g2D.drawImage(image, 0, 0, this) ;
        
    }

    public Image getImage() {
        return image;
    }


}