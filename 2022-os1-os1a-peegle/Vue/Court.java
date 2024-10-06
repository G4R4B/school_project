package Vue;

import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.image.BufferedImage;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseAdapter;
import java.awt.AlphaComposite;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Point;
import java.util.ArrayList;


import javax.swing.JPanel;
import javax.swing.Timer;
import javax.swing.event.MouseInputListener;

import Modele.Ball;
import Modele.Niveau;
import Modele.Pegs;
import Vue.Menu.BoutonMenu;

public class Court extends JPanel implements MouseInputListener, KeyListener {

    private int width;
    private int height;
    public Canon canon;
    private Sceau sceau;
    private Niveau niveau;
    private int toucher;
    private ArrayList<Ball> balls;
    private ArrayList<Pegs> pegs;
    private ArrayList<Pegs> toucherPegs;
    private Background background;
    private int NbDeBall;
    private boolean nbDeBallChange = true;
    private int MaxCombo = 0;
    private Font arcade = ImageImport.arcade;
    private Font rightF;
    private static boolean BallIllimite =false;
    
    public static boolean isBallIllimite() {
        return BallIllimite;
    }

    public static void setBallIllimite(boolean ballIllimite) {
        BallIllimite = ballIllimite;
    }

    private int mouseX = 0;
    private int mouseY = 0;
    private boolean gameOver = false;
    private int ScoreMax;
    private int ComboEncours = 0;
    private int frameCount = 0;
    private int afficageCombo = 0;

    private boolean enPause;

    // Pour l'éditeur de niveaux
    private EditeurNiveaux eN;
    private boolean editMode;
    private Controleur controleur;
    private Point center;
    private Point pressPoint;
    private Pegs pressPeg;
    private int midleXRect;
    private int midleYRect;
    private int widthRectangle;
    private int heightRectangle;
    private int lengthPressToCenter;
    private int lengthPressToCenterRect;

    public Court(int courtWith, int courtHeight, Niveau niveau, Controleur c) {
        controleur = c;
        setOpaque(false);
        width = courtWith;
        height = courtHeight;
        this.niveau = niveau;
        pegs = clonePegs(niveau.getPegs()); // Crée une copie en profondeur des pegs du niveau.
        ScoreMax = niveau.getScoreMax();

        NbDeBall = niveau.getNbrBall() ;
        if (NbDeBall == 0) NbDeBall = 125 ;

        // Par défaut
        enPause = false;
        eN = null;
        editMode = false;
        center = new Point(courtWith/2, courtHeight/2);
        pressPoint = null;
        pressPeg = null;

        // Listeners
        this.addMouseListener(this);
        this.addMouseMotionListener(this);
        this.addKeyListener(this);

        // ArrayLists
        balls = new ArrayList<>();
        // pegs = new ArrayList<>();
        toucherPegs = new ArrayList<>();

        // Canon
        canon = new Canon(this);
        setLayout(null);
        add(canon);
        canon.setVisible(true);

        canon.setBalleATirer(new Ball(0, 0, 0, 0, this));

        // Balls
        toucher = 0;

        // Sceau
        sceau = new Sceau(this);

        animate();
    }

    public BufferedImage getBall() {
        return Ball.getImgBall();
    }

    public boolean getEnPause() {
        return enPause;
    }

    public void setEnPause(boolean enPause) {
        this.enPause = enPause;
    }

    public Niveau getNiveau() {
        return niveau;
    }
    public void seteN(EditeurNiveaux eN) {
        this.eN = eN;
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }

    public ArrayList<Ball> getBalls() {
        return balls;
    }

    public ArrayList<Pegs> getToucherPegs() {
        return toucherPegs;
    }

    public Sceau getSceau() {
        return sceau;
    }

    public void setPegs(ArrayList<Pegs> pegs) {
        this.pegs = pegs;
    }

    public ArrayList<Pegs> getPegs() {
        return pegs;
    }

    public void augmenteNbDeBall() {
        nbDeBallChange = true;
        NbDeBall++;
    }

    public void setBallChanged(boolean b) {
        nbDeBallChange = b;
    }

    public int getNbDeBall() {
        return NbDeBall;
    }

    public boolean nbBallHasChanged() {
        return nbDeBallChange;
    }

    public int getScore() {
        return toucher;
    }

    public int getScoreMax() {
        return niveau.getScoreMax();
    }

    public void setBackground(Background background) {
        this.background = background;
    }

    public int getBallRadius() {
        return (int) Ball.ballRadius;
    }


    public Canon getCanon() {
        return canon;
    }

    public void setEditMode(boolean editMode) {
        this.editMode = editMode;
    }

    public void activerModeEditeur(EditeurNiveaux eN) {
        setEnPause(true);
        seteN(eN);
        setEditMode(true);
    }

    public void setNiveau(Niveau niveau) {
        this.niveau = niveau;
    }

    public ArrayList<Pegs> clonePegs (ArrayList<Pegs> originalPegs) {
        ArrayList<Pegs> clones = new ArrayList<>();
        for (Pegs p : originalPegs) {
            try {
                clones.add((Pegs) p.clone());
            } catch (CloneNotSupportedException e) {
                e.printStackTrace();
            }
        }
        return clones;
    }

    public void animate() {
        final Timer timer = new Timer(10, null);
        timer.addActionListener(new ActionListener() {
            double now = System.nanoTime();
            double last;

            @Override
            public void actionPerformed(ActionEvent e) {
                if (enPause || gameOver)
                    timer.stop(); // Arrêt de tout le timer.
                else {
                    last = System.nanoTime();
                    for (Ball b : balls) {
                        if (b.isPresent())
                            b.updateBall((last - now) * 1.0e-9, sceau);
                    }
                    sceau.move(((last - now) * 1.0e-9));
                    
                    if (!editMode && pegs.size() == 0) {
                        WinPanel pan = new WinPanel(width / 2, height);
                        pan.setLocation(width / 2 - pan.getWidth() / 2, height / 2 - pan.getHeight() / 2);
                        add(pan);
                        enPause = true;
                    }
                    if (!editMode && getNbDeBall() == 0 && balls.size() == 0 ) {
                        LosePanel pan = new LosePanel(width / 2, height);
                        pan.setLocation(width / 2 - pan.getWidth() / 2, height / 2 - pan.getHeight() / 2);
                        add(pan);
                        pan.requestFocusInWindow() ;
                        enPause = true;
                    }
                    for (Pegs peg : pegs) {
                        peg.fonctionDeMouvement((last-now)*1.0e-9);
                    }
                    sceau.move(((last-now)*1.0e-9));
                    repaint();
                    if (!editMode) background.repaint();
                    now = last;
                }
            }
        });
        timer.start();
    }
    
    private void tirer(){
        if (NbDeBall > 0) {
            balls.add(canon.tirer());
            nbDeBallChange = true;
            if ( ! BallIllimite){
                NbDeBall--;
            }
            if (!editMode)
                background.repaint();
        }
    }

    public void askReset(){
        pegs.clear();
        FinDeCampagne pan = new FinDeCampagne(width / 2, height);
        pan.setLocation(width / 2 - pan.getWidth() / 2, height / 2 - pan.getHeight() / 2);
        add(pan);
        pan.requestFocusInWindow() ;
        enPause = true;
    }

    public void updateMetrics() {
        midleXRect = (int)(pressPoint.getX() + (mouseX - pressPoint.getX())/2);
        midleYRect = (int)(pressPoint.getY() + (mouseY - pressPoint.getY())/2);
        widthRectangle = (int) (mouseX - pressPoint.getX());
        heightRectangle = (int) (mouseY - pressPoint.getY());
        lengthPressToCenter = (int) Math.sqrt(Math.pow(pressPoint.getX() - center.getX(), 2) + Math.pow(pressPoint.getY() - center.getY(), 2));
        lengthPressToCenterRect = (int) Math.sqrt(Math.pow(Math.abs(pressPoint.getX() - midleXRect), 2) + Math.pow(Math.abs(pressPoint.getY() - midleYRect), 2));
    }

    public void paint(Graphics g) {

        super.paint(g);
        // init 
        if (rightF == null) {
            rightF = arcade.deriveFont(1000f); // Très grande taille de police par défault
            FontMetrics metrics = g.getFontMetrics(rightF);
            int fontSize = rightF.getSize();
            int textWidth = metrics.stringWidth("Combo x100");
            int textWidthMax = width-150;
            if (textWidth > textWidthMax) {
                double widthRatio = (double) textWidthMax / (double) textWidth;
                rightF = rightF.deriveFont((float) Math.floor(fontSize * widthRatio));
                fontSize = rightF.getSize();
                metrics = g.getFontMetrics(rightF);
            }
        }

        // partie finie
        if (gameOver) return;
        
        // Affichage du sceau
        g.drawImage(sceau.getImageHAUT(), (int) sceau.Xb, (int) sceau.Yh, this);
        
        // Affichage des balles
        g.setColor(Color.BLACK);
        for (Ball ball : balls) {
            if (ball.isPresent()) {
                g.setColor(Color.BLACK);
                g.drawImage(ball.getImage(), (int) ball.ballX, (int) ball.ballY, this);
            }
        }

        // Affichage des combos
        if (!editMode) {
            frameCount++;
            if (ComboEncours != 0) {
                g.setFont(rightF);
                if (ComboEncours>MaxCombo) MaxCombo = ComboEncours;
                if (afficageCombo>5) g.setColor(Color.RED);
                else if (afficageCombo>3) g.setColor(Color.ORANGE);
                else g.setColor(Color.YELLOW);
                if (frameCount>=10) {
                    g.drawString("Combo x"+afficageCombo, (int)150, (int)400);
                    
                    background.repaint(); // Condition pour l'editeur de niveau
                    frameCount = 0;
                    if (afficageCombo < ComboEncours)
                        afficageCombo++;
                    else {
                        ComboEncours = 0;
                        afficageCombo = 0;
                    }
                } else
                    g.drawString("Combo x" + afficageCombo, (int) 150, (int) 400);
            }
        }

        // remove ball hit the ground
        boolean remove = false;
        for (int i = 0; i < balls.size(); i++) {
            if (balls.get(i).getHitGround()) {
                ComboEncours = balls.get(i).getCombo();
                toucher += balls.get(i).getComboScore();
                balls.remove(i);
                remove = true;
            }
        }

        if (remove) {
            for (Pegs peg : pegs) {
                if (peg.getHit() && !toucherPegs.contains(peg)) {
                    toucherPegs.add(peg);
                }
            }
        }

        if (toucherPegs.size() > 0) {
            Pegs peganim = toucherPegs.get(0);
            g.drawOval((int) peganim.getX() - peganim.getRadius(), (int) peganim.getY() - peganim.getRadius(), peganim.getDiametre(), peganim.getDiametre());
            pegs.remove(peganim);
            toucherPegs.remove(peganim);
        }

        // Affichage du sceau
        g.drawImage(sceau.getImageBAS(), (int) sceau.Xb, (int) sceau.Yb, this);

        // Affichage des pegs
        Graphics2D g2d = (Graphics2D) g;   
        for (Pegs peg: pegs) {
            if (peg.getHit()) g2d.drawImage(ImageImport.getImage(peg.getImageStringTouche()), (int) peg.getX() - peg.getRadius(), (int) peg.getY() - peg.getRadius(), peg.getDiametre(), peg.getDiametre(), this);
            else g2d.drawImage(ImageImport.getImage(peg.getImageString()), (int) peg.getX() - peg.getRadius(), (int) peg.getY() - peg.getRadius(), peg.getDiametre(), peg.getDiametre(), this);
            //image pegs toucher
        }
        

        g.setColor(Color.RED);
        // traçage ligne de viser
        if (!enPause) {
            canon.calculCordonneeLigneViser();
            Graphics2D g2DGameview = (Graphics2D) g;
            g2DGameview.setColor(Color.RED);
            float dash1[] = { 20.0f };
            BasicStroke dashed = new BasicStroke(5.0f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER, 10.0f, dash1,
                    0.0f);
            g2DGameview.setStroke(dashed);
            g2DGameview.drawPolyline(canon.getXLigneViser(), canon.getYLigneViser(), 10);
        }

        // Draw preview pour l'editeur de niveaux
        if (editMode && eN.caseActive != null && enPause && !eN.enModif) {
            Pegs pV = eN.caseActive.modeleActuel; // preview transparent
            float alpha = (float) 0.2; // draw at 20% opacity
            AlphaComposite ac = AlphaComposite.getInstance(AlphaComposite.SRC_OVER, alpha);
            g2d.setComposite(ac);
            g2d.drawImage(ImageImport.getImage(pV.getImageString()), (int) pV.getX() - pV.getRadius(), (int) pV.getY() - pV.getRadius(), pV.getDiametre(), pV.getDiametre(), this);
        }

        // Affichage cercle autour des pegs sélectionnées pour l'editeur de niveaux
        if (editMode && enPause && eN.enModif) {
            // g2d.setColor(Color.ORANGE); // Rouge par défault
            for (Pegs peg : eN.pegsSelectionnes) {
                if (editMode && eN.pegsSelectionnes.contains(peg)) g2d.drawOval((int) peg.getX() - peg.getRadius(), (int) peg.getY() - peg.getRadius(), peg.getDiametre(), peg.getDiametre());
            }
        }

        // Affichage rectangle de selection et éléments en son sein
        if (editMode && enPause && eN.enModif && pressPoint != null) {
            // Affichage ligne d'alignement
            switch (eN.valeurAlignement[0]) {
                case 1: // Alignement horizontal
                    g2d.drawLine((int) pressPoint.getX(), midleYRect, mouseX, midleYRect);
                    break;
                case 2: // Alignement vertical
                    g2d.drawLine(midleXRect, (int) pressPoint.getY(), midleXRect, mouseY);
                    break;
                case 3: // Alignement diagonal
                    g2d.drawLine((int) pressPoint.getX(), (int) pressPoint.getY(), mouseX, mouseY);
                    break;
                case 4: // Alignement circulaire autour du centre
                    int radius = lengthPressToCenter;
                    g2d.drawOval((int) (center.getX() - radius), (int) (center.getY() - radius), radius*2, radius*2);
                    break;
                case 5: // Alignement autour du centre du rectangle
                    int radiusToRect =  lengthPressToCenterRect;
                    g2d.drawOval((int) (midleXRect - radiusToRect), (int) (midleYRect - radiusToRect), radiusToRect*2, radiusToRect*2);
                    break;
                case 6: // Alignement sur l'ellipse inscrite dans le rectangle
                    int x = widthRectangle > 0 ? (int) pressPoint.getX() : (int) (pressPoint.getX() + widthRectangle);
                    int y = heightRectangle > 0 ? (int) pressPoint.getY() : (int) (pressPoint.getY() + heightRectangle);
                    g2d.drawOval(x, y, Math.abs(widthRectangle), Math.abs(heightRectangle));
                    break;
                default:
                    break;
            }
            // Affichage éléments en lien avec les fonctions de mouvement
            int l = 5; // longueur croix
            switch (eN.valeurMouvementGlobal[0]) {
                case 1:
                    switch (eN.valeurMouvementC[0]) {
                        case 1, 2:
                            g.drawLine((int) midleXRect-l, (int) midleYRect, (int) midleXRect+l, (int) midleYRect);
                            g.drawLine((int) midleXRect, (int) midleYRect-l, (int) midleXRect, (int) midleYRect+l);
                            break;
                        default:
                            break;
                    }
                    break;
                case 2, 3: // Rotation centrale
                    g.drawLine((int) center.getX()-l, (int) center.getY(), (int) center.getX()+l, (int) center.getY());
                    g.drawLine((int) center.getX(), (int) center.getY()-l, (int) center.getX(), (int) center.getY()+l);
                    break;
                default:
                    break;
            }
            // Affichage rectangle de selection
            float alpha = (float) 0.2; //draw at 20% opacity
            AlphaComposite ac = AlphaComposite.getInstance(AlphaComposite.SRC_OVER,alpha);
            g2d.setComposite(ac);
            g2d.setColor(new Color(67,174,210,255));
            int largeur = (int) (mouseX - pressPoint.getX());
            int hauteur = (int) (mouseY - pressPoint.getY());
            if (largeur < 0 && hauteur < 0) g2d.fillRect(mouseX, mouseY, -largeur, -hauteur);
            else if (largeur > 0 && hauteur < 0) g2d.fillRect((int) pressPoint.getX(), mouseY, largeur, -hauteur);
            else if (largeur < 0 && hauteur > 0) g2d.fillRect(mouseX, (int) pressPoint.getY(), -largeur, hauteur);
            else g2d.fillRect((int) pressPoint.getX(), (int) pressPoint.getY(), largeur, hauteur);
        }
    }



    public void mousePressed(MouseEvent e) {
        // lancer une balle
        if (!enPause && !gameOver) {
           tirer();
        }
        // Sélectionner un peg
        else if (editMode && eN.enModif) {
            boolean sourisSurPeg = false;
            for (Pegs p : niveau.getPegs()) {
                if (p.contains(mouseX, mouseY)) {
                    if (!eN.pegsSelectionnes.contains(p)) {
                        eN.pegsSelectionnes.clear();
                        eN.pegsSelectionnes.add(p);
                        eN.sliderPegSelectionne.setValue(p.getRadius());
                        eN.sliderPegSelectionne.repaint();
                        eN.boutonsModifActifs(true);
                        repaint();
                    }
                    pressPeg = p;
                    sourisSurPeg = true;
                    break;
                }
            }
            // Déselectionner les pegs sélectionnés
            if (!sourisSurPeg) {
                eN.pegsSelectionnes.clear();
                eN.boutonsModifActifs(false);
                pressPoint = new Point(mouseX, mouseY);
                updateMetrics();
            }
        }
        // Placer un peg
        else if (editMode) {
            try {
                niveau.getPegs().add((Pegs) eN.caseActive.modeleActuel.clone());
                pegs.add((Pegs) eN.caseActive.modeleActuel.clone());
            } catch (CloneNotSupportedException e1) {
                e1.printStackTrace();
            }
            repaint();
        }
    }

    public void mouseExited(MouseEvent e) {
        if (editMode && enPause && !eN.enModif) {
            eN.caseActive.modeleActuel.setX(-100); // Fait disparaître le preview du court
            eN.caseActive.modeleActuel.setY(-100);
            repaint();
        }
    }

    public void mouseDragged(MouseEvent e) {
        mouseX = e.getX();
        mouseY = e.getY();
        if (editMode && pressPoint != null) updateMetrics();
        // Déplacement du canon en fonction de la position de la souris
        if (!enPause) canon.DeplacementCanon(e);
        // Déplacement des pegs selectionnés
        else if (editMode && eN.enModif && pressPoint == null) { // pressPoint null --> souris sur peg
            double diffX = mouseX - pressPeg.getX();
            double diffY = mouseY - pressPeg.getY();
            for (Pegs peg : eN.pegsSelectionnes) {
                peg.setX(peg.getX() + diffX);
                peg.setY(peg.getY() + diffY);
                if (peg.getRectCenter() != null)
                peg.getRectCenter().setLocation(peg.getRectCenter().x + diffX, peg.getRectCenter().y + diffY);
            }
            setPegs(clonePegs(niveau.getPegs()));
            repaint();
        // Sélection des pegs contenus dans le rectangle
        } else if (editMode && eN.enModif && pressPoint != null) {
            for (Pegs peg : eN.niveauCree.getPegs()) {
                if (!eN.pegsSelectionnes.contains(peg) && estDansRectangle(peg)) eN.pegsSelectionnes.add(peg);
                if (eN.pegsSelectionnes.contains(peg) && !estDansRectangle(peg)) eN.pegsSelectionnes.remove(peg);
            }
            repaint(); // Aggrandissement du rectangle de sélection
        }
    }

    public boolean estDansRectangle(Pegs peg) {
        return peg.getX() > Math.min(pressPoint.getX(), mouseX) && peg.getX() < Math.max(pressPoint.getX(), mouseX)
        && peg.getY() > Math.min(pressPoint.getY(), mouseY) && peg.getY() < Math.max(pressPoint.getY(), mouseY);
    }

    public void mouseMoved(MouseEvent e) {
        mouseX = e.getX();
        mouseY = e.getY();
        if (editMode && pressPoint != null) updateMetrics();
        // Déplacement du canon en fonction de la position de la souris
        if (!enPause)
            canon.DeplacementCanon(e);
        // Pour faire apparaître un preview du peg qu'on poserait à cet endroit
        else if (editMode && !eN.enModif) {
            eN.caseActive.modeleActuel.setX(mouseX);
            eN.caseActive.modeleActuel.setY(mouseY);
            repaint();
        }
    }

    public void mouseReleased(MouseEvent e) {
        if (editMode && eN.enModif && pressPoint != null) {
            appliquerAlignement(); // Alignement des pegs sélectionnés
            appliquerMouvement(); // Ajout d'une éventuelle fonction de mouvement aux pegs sélectionnés
            pressPoint = null;
            pressPeg = null;
            if (!eN.pegsSelectionnes.isEmpty()) eN.boutonsModifActifs(true);
            repaint();
        }
    }

    public void appliquerAlignement() {
        boolean deplacementPegs = true;
        double coeff1, coeff2, shift1, shift2;
        if (eN.pegsSelectionnes.size() > 0) {
            switch (eN.valeurAlignement[0]) {
                case 0: // Aucun alignement
                    deplacementPegs = false;
                    break;
                case 1: // Alignement horizontal
                    for (Pegs peg : eN.pegsSelectionnes) {
                        int midleY = (int)(pressPoint.getY() + (mouseY - pressPoint.getY())/2);
                        peg.setY(midleY);
                    }
                    if (eN.uniforme.isSelected()) uniformiserEnX(widthRectangle);
                    break;
                case 2: // Alignement vertical
                    for (Pegs peg : eN.pegsSelectionnes) {
                        int midleX = (int)(pressPoint.getX() + (mouseX - pressPoint.getX())/2);
                        peg.setX(midleX);
                    }
                    if (eN.uniforme.isSelected()) uniformiserEnY(heightRectangle);
                    break;
                case 3: // Alignement diagonal
                    if (eN.uniforme.isSelected()) {
                        uniformiserEnX(widthRectangle);
                        uniformiserEnY(heightRectangle);
                    } else {
                        coeff1 = (pressPoint.getY() - mouseY) / (pressPoint.getX() - mouseX);
                        coeff2 = - 1/coeff1;
                        shift1 = - coeff1 * mouseX + mouseY;
                        for (Pegs peg : eN.pegsSelectionnes) {
                            shift2 = - peg.getX()*coeff2 + peg.getY();
                            peg.setX((int) ((shift2 - shift1) / (coeff1 - coeff2)));
                            peg.setY((int) (coeff1 * (shift2 - shift1) / (coeff1 - coeff2) + shift1));
                        }
                    }
                    break;
                case 4: // Alignement circulaire autour du centre
                    uniformiserSurEllipse(center, lengthPressToCenter, lengthPressToCenter);
                    break;
                case 5: // Alignement circulaire autour du centre du rectangle
                    uniformiserSurEllipse(new Point(midleXRect, midleYRect), lengthPressToCenterRect, lengthPressToCenterRect);
                    break;
                case 6: // Alignement circulaire sur ellipse inscrite dans le rectangle
                    uniformiserSurEllipse(new Point(midleXRect, midleYRect), Math.abs(widthRectangle)/2, Math.abs(heightRectangle)/2);
                    break;
                default:
                    break;
            }
        }
        if (deplacementPegs) setPegs(clonePegs(eN.niveauCree.getPegs()));
    }

    public void uniformiserEnX(int length) {
        int ecart = length / (eN.pegsSelectionnes.size()+1);
        for (int i = 0; i < eN.pegsSelectionnes.size(); i++) {
            eN.pegsSelectionnes.get(i).setX((int) (pressPoint.getX() + (i+1)*ecart));
        }
    }

    public void uniformiserEnY(int length) {
        int ecart = length / (eN.pegsSelectionnes.size()+1);
        for (int i = 0; i < eN.pegsSelectionnes.size(); i++) {
            eN.pegsSelectionnes.get(i).setY((int) (pressPoint.getY() + (i+1)*ecart));
        }
    }

    public void uniformiserSurEllipse(Point center, int radiusX, int radiusY) {
        double ecart = 2*Math.PI / eN.pegsSelectionnes.size();
        for (int i = 0; i < eN.pegsSelectionnes.size(); i++) {
            eN.pegsSelectionnes.get(i).setX((int) (center.getX() + Math.cos(ecart*i)*radiusX));
            eN.pegsSelectionnes.get(i).setY((int) (center.getY() + Math.sin(ecart*i)*radiusY));
        }
    }

    public void appliquerMouvement() {
        boolean ajoutMouvementPegs = true;
        for (Pegs peg: eN.pegsSelectionnes) {
            peg.setValeursFctMouvement(new int[] {eN.valeurMouvementGlobal[0], eN.valeurMouvementH[0], eN.valeurMouvementC[0]});
            if (eN.valeurMouvementGlobal[0] != 0) {
                peg.setCourtCenter(center);
                peg.setRadiusToCourtCenter();
                peg.setCourtWidth(width);
                peg.setRectCenter(new Point(midleXRect, midleYRect));
                peg.setRectWidth(widthRectangle);
                peg.setRectHeight(heightRectangle);
                peg.updateRadiusToRectCenter();
            }
            peg.setSpeed(eN.valeurVitesse);
        }
        if (ajoutMouvementPegs) setPegs(clonePegs(eN.niveauCree.getPegs()));
    }

    public void keyPressed(KeyEvent e) {
        switch (e.getKeyCode()) {
            case (KeyEvent.VK_RIGHT):
                canon.deplacementCanon(false);
                break;
            case (KeyEvent.VK_LEFT):
                canon.deplacementCanon(true);
                break;

            case (KeyEvent.VK_ENTER):
            case (KeyEvent.VK_SPACE):
                if (!enPause && !gameOver) {
                    tirer();
                }
                break;
            case (KeyEvent.VK_ESCAPE):
            case (KeyEvent.VK_CONTROL):
                controleur.gameview.launchMenuPause(true); 
                break;
            default:
                break;
        }
    }

    public void keyReleased(KeyEvent e) {}
    public void mouseEntered(MouseEvent e) {}
    public void mouseClicked(MouseEvent e) {}
    public void keyTyped(KeyEvent e) {}

    public class PanelFin extends JPanel{
        int width;
        int height;

        
        PanelFin(int width, int height) {
            this.width = width;
            this.height = height;
            // indépendant de la classe, pour la fin du jeu :
            gameOver = true;
            canon.setVisible(false);
            Court.this.setBorder(null);
            background.setOver(true);
            background.repaint();

            // parametre du Panel :
            setOpaque(false);
            setLayout(null);
            setVisible(true);
            setSize(width, height);
        }

        public void Textentete(String texteEntete,  Graphics g){
            g.setFont(ImageImport.rightSizeArcade(texteEntete, (width * 573) / 781));
            g.setColor(Color.WHITE);
            FontMetrics fm = g.getFontMetrics(g.getFont()) ;
            int offsetX = ((width * 573) / 781) - fm.stringWidth(texteEntete) ;
            int offsetY = fm.getAscent()/2 ;
            g.drawString(texteEntete, (width * 104) / 781 +offsetX, (height * 45) / 876 + offsetY);
        }
    }

    public class LosePanel extends PanelFin{
        BufferedImage LoseScreen;
        BoutonMenu restart ;
        BoutonMenu retour ;
       

        
        LosePanel(int width, int height) {
            super(width, height) ;

            LoseScreen = ImageImport.getImage("Gameview/ResumeScreen.png", width, height);

            int ydepart = (this.getHeight() * 350) / 876;
            int yoffset = (this.getHeight() * 200) / 876;

            restart = new BoutonMenu("Recommencer", (this.getWidth()) / 2, (50*Court.this.getWidth())/520);
            restart.setLocation(this.getWidth() / 2 - restart.getWidth() / 2, ydepart- restart.getHeight()/2);
            restart.setVisible(true);
            restart.addActionListener(e -> {
                controleur.launchGameview(niveau.getDossier());
            });
            add(restart);

            retour = new BoutonMenu("   Quitter   ", (this.getWidth()) / 2, (50*Court.this.getWidth())/520);
            retour.setLocation(this.getWidth() / 2 - retour.getWidth() / 2, ydepart +yoffset - retour.getHeight()/2);
            retour.setVisible(true);
            retour.addActionListener(e -> controleur.launchMenu());
            add(retour);

            setFocusable(true) ;
            addKeyListener(new BoutonMenu.BoutonClavier(new BoutonMenu[]{restart, retour}, ()-> controleur.launchMenu())) ;
            
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            g.drawImage(LoseScreen, 0, 0, this);

            Textentete("Niveau " + niveau.getNom() + " perdu !", g);
        }


    }

    public class WinPanel extends PanelFin {
        BufferedImage WinScreen;
        BufferedImage WinScreenDisable;
        boolean exited;

        
        
        WinPanel(int width, int height) {
            super(width, height) ;

            WinScreen = ImageImport.getImage("Gameview/WinScreen.png", width, height);
            WinScreenDisable = ImageImport.getImage("Gameview/WinScreenDisabled.png", width, height);
            exited = false;

            addMouseListener((MouseListener) new MouseAdapter() {
                public void mouseEntered(MouseEvent evt) {
                    exited = true;
                    repaint();
                }

                public void mouseExited(MouseEvent evt) {
                    exited = false;
                    repaint();
                }

                public void mousePressed(MouseEvent evt) {
                    niveau.setChecked(true);
                    if (niveau.isCampagne()) controleur.setNiveauSuivant();
                    else controleur.launchMenu() ;
                }
            });
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            if (exited)
                g.drawImage(WinScreen, 0, 0, this);
            else
                g.drawImage(WinScreenDisable, 0, 0, this);

           
            Textentete("Niveau " + niveau.getNom() + " fini !", g);

            int x = (width * 50) / 876 ;
            int y =(height * 175) / 876 ;
            g.setFont(ImageImport.rightSizeArcade("Balles Utilisees: 1000", (width * (876-90)) / 876));
            g.setColor(Color.WHITE);
            g.drawString("Score: " + toucher, x, y);  
            y += (height * 75) / 876  ;          
            g.drawString("Balles Restantes: " + NbDeBall, x, y);
            y += (height * 75) / 876  ; 
            g.drawString("Balles Utilisees: " + canon.getNbDeBallTirer(), x, y);
            y += (height * 75) / 876  ;          
            g.drawString("Score Max : " + niveau.getScoreMax(), x, y);
            if (toucher > ScoreMax) {
                y = (height *600) / 876  ;          
                g.drawString("Nouveau score max!!!", x, y);
                niveau.setScoreMax(toucher);
            }
        }
    }

    public class FinDeCampagne extends PanelFin{
        BufferedImage background ;
        BoutonMenu quit ;
        BoutonMenu resetCampagne ;

        FinDeCampagne(int width, int height){
            super(width, height) ;
            background = ImageImport.getImage("Gameview/ResumeScreen.png", width, height);
            
            // boutons
            resetCampagne = new BoutonMenu("Recommencer", (this.getWidth()) / 2, (87*this.getHeight())/876);
            resetCampagne.setLocation(this.getWidth() / 2 - resetCampagne.getWidth() / 2, (this.getHeight() * 350) / 876 );
            resetCampagne.setVisible(true);
            resetCampagne.addActionListener(e -> {
                Niveau.resetAllCheckNiveau(true );
                controleur.setNiveauSuivant();
            });
            add(resetCampagne);
            
            quit = new BoutonMenu("Quitter", (this.getWidth()) / 2, (87*this.getHeight())/876);
            quit.setLocation(this.getWidth() / 2 - quit.getWidth() / 2, (this.getHeight() * 530) / 876);
            quit.setVisible(true);
            quit.addActionListener(e -> {
                controleur.launchMenu() ;
            });
            add(quit);

            setFocusable(true);
            addKeyListener(new BoutonMenu.BoutonClavier(new BoutonMenu[]{resetCampagne, quit}, ()-> controleur.launchMenu())) ;

        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            g.drawImage(background, 0, 0, this) ;

            Textentete("Vous avez fini le jeu !" , g);


            int x = (width * 55) / 876 ;
            int y =(height * 175) / 876 ;
            g.setFont(ImageImport.rightSizeArcade("* Ou bien recommencer la campagne ", (width * (876-90)) / 876));   
            
            g.drawString("Vous avez fini la campagne !", x, y);
            y += (height * 75) / 876  ;          
            g.drawString("Vous pouvez maintenant :", x, y);
            
            y += (height * 75) / 876  ;          
            g.drawString("* Recommencer la campagne", x, y);
            
            
            y =(height * 500) / 876 ;    
            g.drawString("* Ou creer vos propres niveaux", x, y);

        }
    }

    public int getScoreMaxBackground() {
        return niveau.getPegs().size() * 4;
    }
}
