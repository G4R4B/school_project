package Vue.Menu;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.image.BufferedImage;
import java.util.List;

import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.JTextField;
import Modele.Niveau;
import Vue.Controleur;
import Vue.ImageImport;

public class SelectNiveau extends JPanel implements KeyListener{
    
    

    private List<String> allCheckNiveau;
    private int page_act ;
    private boolean campagne ;
    private Controleur controleur ;

    private JPanel[] affichage ;
    private BufferedImage background ;

    private Fleche next ;
    private Fleche previous ;
    private Recherche recherche;

    private JButton btnRetour;

    // choix du type de partie
    private BoutonMenu selectCampagne ;
    private BoutonMenu selectPerso ;
    private BoutonMenu aleatoire ;

    public SelectNiveau(Controleur c) {
        
        controleur = c ;
        
        setBounds(0, 0, controleur.getWidth(), controleur.getHeight());
        c.add(this) ;
        this.setVisible(true); 
        this.setLayout(null);
        
        // setImage background
        background = ImageImport.getImage("Menu/menuBackground.jpg", this.getWidth(), this.getHeight());

        // JButton boutonRetour
        btnRetour = new BoutonMenu("Retour", 200, 50);
        btnRetour.setLocation(40,40);
        btnRetour.addActionListener(e -> controleur.launchMenu());
        add(btnRetour);

        // demande de quoi afficher 
        int middleW = controleur.getWidth()/2 ; 
        int offsetY = 100+ 25 ;
        int debutY = controleur.getHeight()/2 -50 - offsetY ;

        selectCampagne = new BoutonMenu("Campagne", 400, 100);
        selectCampagne.setLocation(middleW-selectCampagne.getWidth()/2, debutY);
        selectCampagne.addActionListener(e -> setSelecteur(true) );
        add(selectCampagne);
        
        selectPerso = new BoutonMenu("Perso", 400, 100);
        selectPerso.setLocation(middleW-selectPerso.getWidth()/2, debutY+offsetY);
        selectPerso.addActionListener(e -> setSelecteur(false) );
        add(selectPerso);
        aleatoire = new BoutonMenu("Aleatoire", 400, 100);
        aleatoire.setLocation(middleW-aleatoire.getWidth()/2, debutY+2*offsetY);
        aleatoire.addActionListener(e -> controleur.launchGameview("aleatoire") );
        add(aleatoire);

        this.setFocusable(true);
        this.addKeyListener(new BoutonMenu.BoutonClavier(new BoutonMenu[]{selectCampagne, selectPerso, aleatoire}, ()-> controleur.launchMenu()));
        this.requestFocusInWindow() ;
    }

    private void setSelecteur(boolean campagne){
        if (selectCampagne != null) this.remove(selectCampagne);
        if (selectPerso != null) this.remove(selectPerso);
        if (aleatoire != null) this.remove(aleatoire);

        this.campagne = campagne ;
        allCheckNiveau = Niveau.getAllCheckNiveau(campagne) ;

        page_act = 0 ;

        int largeurFleche = 45 ;
        int hauteurFleche = 50 ;
        int x = this.getWidth()-100 ;
        int y = this.getHeight()-100 ;
        // définir place des boutons 
            next = new Fleche(true, largeurFleche, hauteurFleche);
            previous = new Fleche(false, largeurFleche, hauteurFleche) ;
            recherche = new Recherche(x-300,50, campagne);
            next.setBounds(x, y, largeurFleche, hauteurFleche);
            previous.setBounds( x - (next.getWidth() + 15) , y, largeurFleche, hauteurFleche);
            this.add(previous);
            this.add(next) ;
            this.add(recherche);
        afficherPage(page_act);
        this.addKeyListener(this);
        this.requestFocusInWindow() ;
    }

    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        g.drawImage(background, 0, 0, this);
    }

    private void afficherPage(int page){
        if (affichage != null) for (JPanel	pan : affichage) if (pan != null) this.remove(pan); //nettoye les anciens images et texte
        affichage  = new JPanel[6] ;

        int espacementLargeurPres = this.getWidth()/13 ;
        int largeurPres = espacementLargeurPres*3 ;
        int milieu  = this.getHeight() /2 ;
        int hauteur_pres  = milieu - 150  ;
        int x,y ;

        // affichage icone plus bouton de selections
        String[] aafficher = getNamePage(page) ;
        for(int i = 0 ; i < aafficher.length ; i++){
            affichage[i] = new PresNiveau(aafficher[i], largeurPres, hauteur_pres) ;
            x = (1+(i%3)*4)*espacementLargeurPres ;
            if (i < 3) y = milieu - affichage[i].getHeight() -25 ;
            else y  = milieu +25 ;
            affichage[i].setBounds(x, y, largeurPres, affichage[i].getHeight()); 
            this.add(affichage[i]) ;
            affichage[i].setVisible(true);
        }

        // affichage des boutons retour et suivant :
        previous.setVisible(page > 0) ;
        next.setVisible((page+1)*6 < allCheckNiveau.size());
        this.repaint();
        this.revalidate();
    }

    private String pathIcone(){
        return "IconeNiveau/"+ (campagne? "Campagne/" : "Perso/") ;
    }

    private String[] getNamePage(int page){
        int NbrElement = allCheckNiveau.size() - page*6 ;
        if (NbrElement > 6) NbrElement  =6 ;
        String[] ret = new String[NbrElement] ;
        for (int i = 0 ; i < ret.length ;i++){
            ret[i] = allCheckNiveau.get(page*6 + i);
        }
        return ret ;
    }

    class Fleche extends JButton{
        Icon imageBlanche;
        Icon imageJaune;

        Fleche(boolean next, int width, int height) {
            imageBlanche = new ImageIcon(ImageImport.getImage("Menu/Fleche/"+ (next?"D":"G") + " blanche.png", width, height));
            imageJaune = new ImageIcon(ImageImport.getImage("Menu/Fleche/"+ (next?"D":"G") + " jaune.png", width, height));

            // enlever tout les contours du JButton ne laisse que l'image
            setBorderPainted(false); 
            setContentAreaFilled(false); 
            setFocusPainted(false); 
            setOpaque(false);
            addMouseListener((MouseListener) new MouseAdapter() {
                public void mouseEntered(MouseEvent evt) {Fleche.this.setIcon(imageJaune);}
                public void mouseExited(MouseEvent evt) {Fleche.this.setIcon(imageBlanche);}
                public void mouseClicked(MouseEvent evt) {   
                    if (next) afficherPage(++page_act);
                    else afficherPage(--page_act);
                }
            });
            setIcon(imageBlanche);
        }
        
    }
    class Recherche extends JTextField{
        private String lastSearch ;
        private String holder ;

        Recherche(int width, int height, boolean campagne){
            setBounds(width, height, 300, 45);
            lastSearch = "" ;
            holder = "Rechercher" ;
            setForeground(Color.GRAY);
            setText(holder);
            addFocusListener(new FocusListener() {
                @Override
                public void focusGained(FocusEvent e) {
                    if (Recherche.this.getText().equals(holder)) {
                        Recherche.this.setForeground(Color.BLACK);
                        Recherche.this.setText("");
                    }
                }
                @Override
                public void focusLost(FocusEvent e) {
                    if (Recherche.this.getText().isEmpty()) {
                        Recherche.this.setForeground(Color.GRAY);
                        Recherche.this.setText(holder);
                    }
                }
            });
            
            addActionListener(e -> {
                String nom = getText() ;
                if ( ! nom.equals(lastSearch)){ //évite de faire plusiseurs fois la meme recherche
                    allCheckNiveau = Niveau.RechercheCheckNiveau(campagne, nom);
                    page_act = 0 ;
                    afficherPage(page_act);
                    lastSearch = nom ;
                }
                SelectNiveau.this.requestFocusInWindow() ;
            });

            // amélioration du style :
            setHorizontalAlignment(JTextField.CENTER);
        }
    }

    class PresNiveau extends JPanel {

        private BufferedImage apercu ;
        private BufferedImage cadre ;
        private BoutonMenu button ;
        private BufferedImage check;
        private BufferedImage etoile;
        private double formatImage = 520/1080.0 ;

        PresNiveau(String nomNiveau, int largeurPres, int hauteur_pres) {

            setLayout(new BoxLayout(this, BoxLayout.PAGE_AXIS));
            setOpaque(false);
            int hauteurBouton  = 40;
            int hauteurPhoto = Math.min(hauteur_pres - hauteurBouton-7, (int)(formatImage*largeurPres)) ;

            JPanel invisiblePhoto = new JPanel() ;
            invisiblePhoto.setSize(largeurPres, hauteurPhoto);
            invisiblePhoto.setOpaque(false);
            (invisiblePhoto).addMouseListener((MouseListener) new MouseAdapter() {
                public void mouseEntered(MouseEvent evt) {button.setCouleur(true);}
                public void mouseExited(MouseEvent evt){button.setCouleur(false);}
                public void mouseClicked(MouseEvent evt){controleur.launchGameview((campagne? "Campagne/" : "Perso/") + nomNiveau.substring(0, nomNiveau.length()-2));}
            });
            add(invisiblePhoto); //ajout d'un bloc pour l'image et l'affichage du layout
            button = new BoutonMenu(nomNiveau.substring(0, nomNiveau.length()-2), hauteurBouton*4, hauteurBouton);
            if (nomNiveau.charAt(nomNiveau.length()-2) == '1'){
                check = ImageImport.getImage("Menu/Check.png", 7);
            }
            etoile = ImageImport.getImage("Menu/etoiles" + nomNiveau.charAt(nomNiveau.length()-1) + "Score.png" , 20);
            button.addActionListener(e -> controleur.launchGameview((campagne? "Campagne/" : "Perso/") + nomNiveau.substring(0, nomNiveau.length()-2)));
            button.setVisible(true);
            button.setAlignmentX(Box.CENTER_ALIGNMENT);
            add(button);
            setSize(largeurPres, hauteurPhoto+hauteurBouton+10 + etoile.getHeight());

            apercu = ImageImport.getImage(pathIcone()+nomNiveau.substring(0, nomNiveau.length()-2)+".png", largeurPres,hauteurPhoto);
            cadre = ImageImport.getImage("Menu/CadreCampagne.png", largeurPres,hauteurPhoto);
        }
        
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            // afficher background
            g.drawImage(apercu, 0, 0, apercu.getWidth(), apercu.getHeight(), this);
            g.drawImage(cadre, 0, 0, cadre.getWidth(), cadre.getHeight(), this);
            if (check != null) g.drawImage(check, cadre.getWidth()/2 - check.getWidth() /2, cadre.getHeight()/2 - check.getHeight() /2 , check.getWidth(), check.getHeight(), this);
            g.drawImage(etoile, cadre.getWidth()/2 - etoile.getWidth() /2, cadre.getHeight() , etoile.getWidth(), etoile.getHeight(), this);
        }
    }

    public void keyPressed(KeyEvent e) {
        switch (e.getKeyCode()){
            case (KeyEvent.VK_RIGHT) :
                if ((page_act+1)*6 < allCheckNiveau.size()) afficherPage(++page_act);
                break ;
            case (KeyEvent.VK_LEFT) :
                if (page_act > 0) afficherPage(--page_act);
                break ;
            case (KeyEvent.VK_ESCAPE) :
                btnRetour.doClick();
                break ;
            case (KeyEvent.VK_BACK_SPACE) :
                recherche.requestFocusInWindow() ; //remet le focus sur la zone de recherche
                break ;
            default :
                break ;
        }
    }

    public void keyTyped(KeyEvent e) {}
    public void keyReleased(KeyEvent e) {}
}
