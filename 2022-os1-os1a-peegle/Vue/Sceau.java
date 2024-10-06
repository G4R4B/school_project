package Vue;
import Modele.*;

import java.awt.image.BufferedImage;

public class Sceau{
    public final int longeur = 140; // m
    public final int hauteur = 70;
    public double speedX = 100; // m

    private int bordure = (longeur * 65) / 405;

    public double Xb, Yb; // m
    public double Xh, Yh; // m
    private Court court;
    private BufferedImage imageBAS,imageHAUT; 

    Sceau(Court court){
        this.court = court;
        Xb = court.getWidth()/2 - longeur/2;
        Yb = court.getHeight() - (hauteur);

        Xh = court.getWidth()/2 - longeur/2;
        Yh = court.getHeight() - (hauteur);

        imageBAS = ImageImport.getImage("Gameview/bucketBAS.png", longeur, hauteur);
        imageHAUT = ImageImport.getImage("Gameview/bucketHAUT.png", longeur, hauteur);
        
    }
    public BufferedImage getImageHAUT(){
        return imageHAUT;
    }

    public BufferedImage getImageBAS(){
        return imageBAS;
    }


    public void move(double deltaT){
        double nextXb = Xb + deltaT * speedX;

        if (touchedWallX(nextXb)){
            speedX = -speedX;
            nextXb = Xb + deltaT * speedX;
        };
        Xb = nextXb;
        Xh=nextXb;
    }

    public boolean inside(Ball b){
        return Xb + bordure <= b.nextBallX && b.nextBallX + Ball.ballRadius*2 <= Xb + longeur - bordure &&
        Yb  <= b.nextBallY && b.nextBallY <= Yb + hauteur;

    }

    public boolean touchedWallX(double nextX){
        return nextX < 0 || nextX> court.getWidth() - longeur;
    }
    public boolean toucheBordureSceau(Ball b){
        return ((Xb <= b.nextBallX + Ball.ballRadius*2  && b.nextBallX   <= Xb + bordure) || (Xb + longeur - bordure  <= b.nextBallX + Ball.ballRadius*2  && b.nextBallX <= Xb  + longeur) ) && 
        Yb <= b.nextBallY && b.nextBallY <= Yb + hauteur; //hardcoding pour toucher plus bas
    }

    public Court getCourt(){
        return court;
    }
}