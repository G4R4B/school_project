package Modele;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.geom.RoundRectangle2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import javax.imageio.ImageIO;
import Vue.ImageImport;

public class Niveau {

    private static String dosierSauvegarde = "Niveau/";
    private static String nomExtension = ".pegs";

    private ArrayList<Pegs> pegs;
    private int nbBillesInitiales;

    private int score1Etoiles;
    private int score2Etoiles;
    private int score3Etoiles;
    
    private boolean campagne;
    
    private String nom;
    private boolean checked;
    private int ScoreMax;
    
    public int getScore1Etoiles() {
        return score1Etoiles;
    }

    public int getScore2Etoiles() {
        return score2Etoiles;
    }

    public int getScore3Etoiles() {
        return score3Etoiles;
    }
    public boolean isCampagne() {
        return campagne;
    }

    public ArrayList<Pegs> getPegs() {
        return pegs;
    }
    public int getNbrBall(){return nbBillesInitiales ;}

    public void setNom(String nom) {
        this.nom = nom;
    }

    public void setPegs(ArrayList<Pegs> pegs) {
        this.pegs = pegs;
    }
    
    public void setNbBillesInitiales(int nbBillesInitiales) {
        this.nbBillesInitiales = nbBillesInitiales;
    }

    public void isCampagne(boolean campagne) {
        this.campagne = campagne;
    }

    public String getNom() {
        return nom;
    }

    public String getDossier() {
        return (campagne ? "Campagne/" : "Perso/") + getNom();
    }

    public Niveau(String nom) {
        this.nom = nom;
        pegs = new ArrayList<>();
    }

    public int getScoreMax() {
        return ScoreMax;
    }

    public void setScoreMax(int newMax) {
        if(nom == "Aleatoire") return ;
        if (newMax < ScoreMax)
            return;
        setValueAtIndex(8, newMax);
        ScoreMax = newMax;
    }

    public void setChecked(boolean checked) {
        if(nom == "Aleatoire") return ;
        this.checked = checked;
        setValueAtIndex(7, checked ? 1 : 0);
    }

    public void setValueAtIndex(int index, int value) {
        List<String> docString = new ArrayList<String>();
        try {
            // modifie la premiere ligne
            Scanner sc = new Scanner(new File(dosierSauvegarde + getDossier() + ".pegs"));
            String[] entete = sc.next().split(";");
            entete[index] = String.valueOf(value);
            String temp = "";
            for (int i = 0; i < entete.length - 1; i++) {
                temp += entete[i] + ";";
            }
            temp += entete[entete.length - 1];
            docString.add(temp);
            while (sc.hasNext())
                docString.add(sc.next());
            sc.close();

            // ecriture
            PrintWriter file = new PrintWriter(dosierSauvegarde + getDossier() + nomExtension);
            for (String line : docString)
                file.println(line);
            file.close();
        } catch (Exception e) {
            System.out.println(e);
        }
    }

    public void setBasic(){
        this.score1Etoiles = this.pegs.size();
        this.score2Etoiles = 2 * this.pegs.size();
        this.score3Etoiles = 3 * this.pegs.size();
        this.ScoreMax = 1;
    }

    public static Niveau NiveauAleatoire(int widthCourt, int heightCourt, int diametrePegs) {
        Niveau nv = new Niveau("Aleatoire");
        nv.campagne = false ;
        int nbrPegs = randInt(60, 200); // aproximatif
        int espaceMinEntre2Pegs = (int) 2.5 * Ball.ballRadius;
        int x, y;

        int debutHeight = heightCourt / 4; // evite d'avoir des balles trop hautes
        int finHeight = heightCourt - 50 ; 

        // segemente l'aire de jeux en carré le plus petit possible tel que les
        // contraintes soit respecté
        int nbrSegW = (int) (widthCourt / (espaceMinEntre2Pegs + diametrePegs)) ;
        int nbrSegH = (int) ((finHeight - debutHeight) / (espaceMinEntre2Pegs + diametrePegs));

        int nbrSegParPegs = (int) (((nbrSegH - 1) * (nbrSegW - 1)) / nbrPegs); // Nombre de segmentation pour chaque
                                                                               // pegs, permet de savoir la probabilité
                                                                               // d'avoir un pegs dans ce carré

        for (int w = 0; w < nbrSegW - 1; w++) {
            for (int h = 0; h < nbrSegH - 1; h++) {
                if (randInt(1, nbrSegParPegs) == 1) { // placer un élément au hasard
                    x = (int) ((w + 0.5) * (widthCourt / (double) nbrSegW));
                    y = (int) ((h + 0.5) * ((finHeight - debutHeight) / (double) nbrSegH) + debutHeight);
                    nv.pegs.add(new Pegs(x, y, diametrePegs/2, randInt(1, 4)));
                }
            }
        }

        nv.removeNotReachable(widthCourt, heightCourt);
        nv.setBasic();
        nv.setNbBillesInitiales(10);
        return nv;
    }

    public static int randInt(int a, int b) {
        return (new SecureRandom()).nextInt(b - a + 1) + a;
    }

    public static void createIconeNiveau(String niveau, boolean campagne) {
        int width = 1080;
        int height = 520;

        Niveau nv = importPegles((campagne ? "Campagne/" : "Perso/") + niveau, width, height);
        BufferedImage tempImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);
        Graphics g = (tempImage.createGraphics());
        Graphics2D g2d = (Graphics2D) g;
        g2d.setColor(Color.white);
        g2d.fill(new RoundRectangle2D.Float(0, 0, width, height, 60, 60));

        for (Pegs peg : nv.getPegs()) {
            g2d.drawImage(ImageImport.getImage(peg.getImageString()), (int) peg.getX() - peg.getRadius(), (int) peg.getY() - peg.getRadius(), 
                peg.getDiametre(), peg.getDiametre(), null);
        }

        try {
            ImageIO.write(tempImage, "png",
                    new File("Vue/Image/IconeNiveau/" + (nv.campagne ? "Campagne/" : "Perso/") + nv.getNom() + ".png"));
        } catch (Exception ex) {
            System.out.println("Impossible d'enregistrer l'image.");
            System.out.println(ex);
        }

        // ajout dans ImportImage si actif
        if (ImageImport.isAtif()) {
            ImageImport.addImage("IconeNiveau/" + nv.getDossier() + ".png");
        }

    }

    public static void resetAllCheckNiveau(boolean campagne) {
        String[] atraiter = new File(dosierSauvegarde + (campagne ? "Campagne" : "Perso")).list();
        for (String nom : atraiter) {
            List<String> docString = new ArrayList<String>();
            try {
                // modifie la premiere ligne
                Scanner sc = new Scanner(new File(dosierSauvegarde + (campagne ? "Campagne/" : "Perso/") + nom));
                String[] entete = sc.next().split(";");
                // valeur à modifier
                entete[7] = String.valueOf(0);
                entete[8] = String.valueOf(1);
                String temp = "";
                for (int i = 0; i < entete.length - 1; i++) {
                    temp += entete[i] + ";";
                }
                temp += entete[entete.length - 1];
                docString.add(temp);
                while (sc.hasNext())
                    docString.add(sc.next());
                sc.close();

                // ecriture
                PrintWriter file = new PrintWriter(dosierSauvegarde + (campagne ? "Campagne/" : "Perso/") + nom);
                for (String line : docString)
                    file.println(line);
                file.close();
            } catch (Exception e) {
                System.out.println(e);
            }
        }
    }

    public void removeNotReachable(int width, int height){
        List<Pegs> remove = new ArrayList<>() ;
        for (Pegs p : pegs) {
            if (p.getX() >width || p.getX()<0 || p.getY() > (9*height)/10 || p.getY()< height/4  ) remove.add(p) ;
        }
        pegs.removeAll(remove) ;
    }


    public static List<String> getAllCheckNiveau(boolean campagne) {
        String[] atraiter = new File(dosierSauvegarde + (campagne ? "Campagne" : "Perso")).list();
        List<String> ret = new ArrayList<>();
        for (int i = 0; i < atraiter.length; i++) {
            try (Scanner save = new Scanner(
                    new File(dosierSauvegarde + (campagne ? "Campagne" : "Perso") + "/" + atraiter[i]))) {
                String[] line = save.nextLine().split(";");
                int scoreetoile = Integer.parseInt(line[8]) >= Integer.parseInt(line[5]) ? 3
                        : (Integer.parseInt(line[8]) >= Integer.parseInt(line[4]) ? 2
                                : (Integer.parseInt(line[8]) >= Integer.parseInt(line[3]) ? 1 : 0));
                ret.add(atraiter[i].substring(0, atraiter[i].length() - 5) + line[7] + scoreetoile); // ajoute le check
                                                                                                     // du niveau au nom
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
        }
        return ret;
    }

    public static List<String> getAllNameNiveau(boolean campagne) {
        String[] atraiter = new File(dosierSauvegarde + (campagne ? "Campagne" : "Perso")).list();
        List<String> ret = new ArrayList<>();
        for (int i = 0; i < atraiter.length; i++) {
            ret.add(atraiter[i].substring(0, atraiter[i].length() - 5));
        }
        return ret;
    }

    public static List<String> getAllNameNiveau() {
        List<String> tout = getAllNameNiveau(true);
        tout.addAll(getAllNameNiveau(false));
        return tout;
    }

    // enregistrement d'un niveau

    public void save(int widthCourt, int heightCourt) {
        if(nom == "Aleatoire") return ;
        // this.removeNotReachable(widthCourt, heightCourt);
        // save les lignes de l'array list dans un fichier csv
        PrintWriter file;
        try {
            file = new PrintWriter(dosierSauvegarde + getDossier() + nomExtension);
            setBasic();

            // premiere ligne d'info :
            String ligne = String.valueOf(widthCourt) + ";"
                    + String.valueOf(heightCourt) + ";"
                    + String.valueOf(nbBillesInitiales) + ";"
                    + String.valueOf(score1Etoiles) + ";"
                    + String.valueOf(score2Etoiles) + ";"
                    + String.valueOf(score3Etoiles) + ";"
                    + String.valueOf(campagne ? "1" : "0") + ";"
                    + String.valueOf(checked ? "1" : "0") + ";"
                    + String.valueOf(ScoreMax);
            file.println(ligne);

            // remplacer par les valeurs à enregistrer
            for (Pegs peg : pegs) {
                ligne = String.valueOf(peg.getX()) + ";"
                        + String.valueOf(peg.getY()) + ";"
                        + String.valueOf(peg.getRadius()) + ";"
                        + String.valueOf(peg.getCouleur());
                if (peg.ifValeurEdit()){
                    int[] tab = peg.getValeursFctMouvement();
                    ligne += ";" + String.valueOf(tab[0]) + ";" + String.valueOf(tab[1]) + ";" + String.valueOf(tab[2]);
                    ligne += ";" + String.valueOf(peg.getRectCenter().x) + ";" + String.valueOf(peg.getRectCenter().y) + ";" + String.valueOf(peg.getRectWidth()) + ";" + String.valueOf(peg.getRectHeight());
                }
                file.println(ligne);

            }
            file.close();
            // enregistrement réussi
        } catch (FileNotFoundException e) {
            System.out.println("La sauvegarde a raté");
            e.printStackTrace();
        }

        // update l'icone du niveau
        createIconeNiveau(this.getNom(), this.campagne);
    }

    public static Niveau importPegles(String name, int widthCourt, int heightCourt) {
        Niveau nv = new Niveau(name.split("/")[name.split("/").length - 1]);// permet de récupéré uniquement le nom et
                                                                            // pas le chemin d'accés

        try (Scanner save = new Scanner(new File(dosierSauvegarde + name + nomExtension))) {
            String[] line = save.nextLine().split(";");

            // obtenir les valeurs de réajustement des des pegs pour qu'il s'adepete à la
            // nouvelle taille de l'écran
            double reajustementH = widthCourt / Double.valueOf(line[0]);
            double reajustementV = heightCourt / Double.valueOf(line[1]);

            // remise des valeurs de Niveau :
            nv.nbBillesInitiales = Integer.valueOf(line[2]);
            nv.score1Etoiles = Integer.valueOf(line[3]);
            nv.score2Etoiles = Integer.valueOf(line[4]);
            nv.score3Etoiles = Integer.valueOf(line[5]);
            nv.campagne = line[6].equals("1") ? true : false;
            nv.checked = line[7].equals("1") ? true : false;
            nv.ScoreMax = Integer.valueOf(line[8]);

            // creation des pegs en fonction des infos que on a
            // update des nouveau coordonnées en fonction de la taille de l'écran actuel
            while (save.hasNextLine()) {
                line = save.nextLine().split(";");
                int x = (int) (reajustementH * Double.valueOf(line[0]));
                int y = (int) (reajustementV * Double.valueOf(line[1]));
                int radius = (int) (Double.valueOf(line[2]) * Math.min(reajustementH, reajustementV));
                int couleur = Integer.valueOf(line[3]);
                

                Pegs ajouter = new Pegs(x, y, radius, couleur);
                nv.pegs.add(ajouter);
                if (line.length > 4) { // si il y a des valeurs de fonction de mouvement (pour les pegs mobiles)
                int[] valeursFctMouvement = new int[3];
                for (int i = 0; i < 3; i++) {
                    valeursFctMouvement[i] = Integer.valueOf(line[4 + i]);
                }
                Point rectCenter = new Point(Integer.valueOf(line[7]), Integer.valueOf(line[8]));
                int rectWidth = Integer.valueOf(line[9]);
                int rectHeight = Integer.valueOf(line[10]);
                ajouter.setRect(rectCenter, rectWidth, rectHeight, widthCourt, heightCourt);
                ajouter.setValeursFctMouvement(valeursFctMouvement);
            }
            }

            save.close();
        } catch (NumberFormatException | FileNotFoundException e) {
            System.out.println("Le nom de fichier ne coorespond pas à un fichier existant");
            e.printStackTrace();
        }
        // return un objet de type
        return nv;
    }

    public static List<String> RechercheCheckNiveau(boolean campagne2, String nom2) {
        List<String> ret = new ArrayList<>();
        for (String name : getAllCheckNiveau(campagne2)) {

            if ((name.toLowerCase()).contains(nom2.toLowerCase())) {
                ret.add(name);
            }
        }
        return ret;
    }

    public static String getNiveauSuivant() {
        List<String> tout = getAllCheckNiveau(true);
        for (int i = 0; i < tout.size(); i++) {
            if (tout.get(i).charAt(tout.get(i).length() - 2) == '0') {
                return tout.get(i).substring(0, tout.get(i).length() - 2);
            }
        }
        return null;
    }

}
