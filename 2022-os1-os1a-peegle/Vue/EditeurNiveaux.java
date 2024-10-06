package Vue;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Cursor;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.MouseEvent;
import java.util.ArrayList;
import java.util.Hashtable;

import javax.swing.BorderFactory;
import javax.swing.ButtonGroup;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JPanel;
import javax.swing.JRadioButtonMenuItem;
import javax.swing.JSlider;
import javax.swing.JTextField;
import javax.swing.UIManager;
import javax.swing.event.MouseInputListener;
import Modele.Ball;
import Modele.Niveau;
import Modele.Pegs;
import Vue.Menu.BoutonMenu;

public class EditeurNiveaux extends JPanel {

    int width;
    int height;

    // Court
    Court court;
    private int courtWidth;
    private int courtHeight;
    Niveau niveauCree;
    CasePeg caseActive;
    ArrayList<Pegs> pegsSelectionnes;
    boolean enModif;

    JSlider sliderPegSelectionne;
    BoutonCouleur bleu;
    BoutonCouleur rouge;
    BoutonCouleur violet;
    BoutonCouleur vert;
    JButton croix;
    JButton modif;
    int[] valeurAlignement;
    int[] valeurMouvementGlobal;
    int[] valeurMouvementH;
    int[] valeurMouvementC;
    int valeurVitesse;
    int largeurBouton;
    CasePeg casePegBleu;
    CasePeg casePegRouge;
    CasePeg casePegViolet;
    CasePeg casePegVert;
    JTextField nomNiveau;
    JCheckBox uniforme;
    JCheckBox campagne;
    JMenuBar menuBar;
    RadioButtonValue aucunAlignement;
    RadioButtonValue aucuneFonction;
    JSlider sliderSpeedPegs;
    JSlider sliderNbBallesInitial;

    EditeurNiveaux(Controleur controleur) {
        width = controleur.getWidth();
        height = controleur.getHeight();
        setLayout(null);
        setSize(width, height);

        niveauCree = new Niveau("enAttente");
        niveauCree.isCampagne(false);
        pegsSelectionnes = new ArrayList<>();

        // JMenuBar menuBar
        menuBar = new JMenuBar();
        int heightMenuBar = 30;
        menuBar.setBounds(0, 0, width, heightMenuBar);
        add(menuBar);

        // Court
        courtWidth = width * 5/6;
        courtHeight = height * 5/6;
        court = new Court(courtWidth, courtHeight, niveauCree, controleur);
        court.activerModeEditeur(this);
        court.setBorder(BorderFactory.createLineBorder(Color.BLACK));
        court.setBounds(0, heightMenuBar, courtWidth, courtHeight);
        court.setVisible(true);
        add(court, BorderLayout.CENTER);

        largeurBouton = courtHeight * 1/16;

        // JMenu Editeur
        JMenu menuEditeur = new JMenu("Editeur");
        menuEditeur.setBounds(0, 0, 75, heightMenuBar);
        menuBar.add(menuEditeur);

        // JButton back
        JButton back = new JButton("Retour");
        menuEditeur.add(back);
        back.addActionListener(e -> {menuEditeur.getPopupMenu().setVisible(false); controleur.launchMenu();});

        // JButton newLevel
        JButton newLevel = new JButton("Nouveau");
        newLevel.addActionListener(e -> reset());
        menuEditeur.add(newLevel);

        // JButton save
        JButton save = new JButton("Sauvegarder");
        save.setEnabled(false);
        menuEditeur.add(save);
        save.addActionListener(e-> niveauCree.save(courtWidth, courtHeight));

        // JMenu Niveau
        JMenu menuNiveau = new JMenu("Niveau");
        menuNiveau.setBounds(75, 0, 75, heightMenuBar);
        menuBar.add(menuNiveau);

        // JCheckBox campagne
        campagne = new JCheckBox("Campagne", false);
        campagne.setBounds((width - courtWidth) + 5, courtHeight * 1/16 + 20, courtHeight * 2/16, courtHeight * 1/16);
        campagne.addItemListener(new ItemListener() {    
            public void itemStateChanged(ItemEvent e) {           
                if (e.getStateChange()==1) niveauCree.isCampagne(true);
                else niveauCree.isCampagne(false);
            }    
            });   
        menuNiveau.add(campagne);
        menuNiveau.addSeparator();

        // JTextField nomNiveau
        String[] placeHolders = new String[]{" Nom du niveau", " Nom déjà utilisé"};
        nomNiveau = new JTextField(placeHolders[0]);
        nomNiveau.setForeground(Color.GRAY);
        nomNiveau.addFocusListener(new FocusListener() {
            String currentHolder;
            public void focusGained(FocusEvent e) {
                for (String string : placeHolders) {
                    if (nomNiveau.getText().equals(string)) {
                        nomNiveau.setForeground(Color.BLACK);
                        currentHolder = nomNiveau.getText();
                        nomNiveau.setText("");
                    }
                }
            }
            public void focusLost(FocusEvent e) {
                if (nomNiveau.getText().isEmpty()) {
                    nomNiveau.setForeground(Color.GRAY);
                    nomNiveau.setText(currentHolder);
                }
            }
        });
        menuNiveau.add(nomNiveau);

        // JButton save Nom
        JButton saveNom = new JButton("Valider nom");
        menuNiveau.add(saveNom);
        saveNom.addActionListener(e -> {
            if (!Niveau.getAllNameNiveau().contains(nomNiveau.getText())
                && !nomNiveau.getText().equals(placeHolders[0])
                && !nomNiveau.getText().equals(placeHolders[1])) {
                niveauCree.setNom(nomNiveau.getText());
                save.setEnabled(true);
            }
            else nomNiveau.setText(placeHolders[1]);
        });
        menuNiveau.addSeparator();

        // JLabel nbBallesInitial
        JLabel labelNbBallesInitial = new JLabel("Nombre de balles initial :");
        menuNiveau.add(labelNbBallesInitial);

        Hashtable<Integer, JLabel> labelTableBallesInitiales = new Hashtable<Integer, JLabel>();
        labelTableBallesInitiales.put(0, new JLabel("0"));
        labelTableBallesInitiales.put(5, new JLabel("5"));
        labelTableBallesInitiales.put(10, new JLabel("10"));
        labelTableBallesInitiales.put(15, new JLabel("15"));
        labelTableBallesInitiales.put(20, new JLabel("20"));
        labelTableBallesInitiales.put(25, new JLabel("25"));
        labelTableBallesInitiales.put(30, new JLabel("30"));
        labelTableBallesInitiales.put(35, new JLabel("35"));
        labelTableBallesInitiales.put(40, new JLabel("40"));
        labelTableBallesInitiales.put(45, new JLabel("45"));
        labelTableBallesInitiales.put(50, new JLabel("50"));

        // JSpinner spinnerNbBallesInitial
        sliderNbBallesInitial = new JSlider(5, 50, 10);
        sliderNbBallesInitial.setMinorTickSpacing(1);
        sliderNbBallesInitial.setMajorTickSpacing(5);
        sliderNbBallesInitial.setPaintTicks(true);
        sliderNbBallesInitial.setLabelTable(labelTableBallesInitiales);
        sliderNbBallesInitial.setPaintLabels(true);
        niveauCree.setNbBillesInitiales(10);
        sliderNbBallesInitial.addChangeListener(e -> niveauCree.setNbBillesInitiales(sliderNbBallesInitial.getValue()));
        menuNiveau.add(sliderNbBallesInitial);

        // JMenu alignement
        JMenu alignement = new JMenu("Alignement");
        valeurAlignement = new int[1];
        ButtonGroup groupAlignement = new ButtonGroup();
        alignement.setBounds(150, 0, 100, heightMenuBar);
        menuBar.add(alignement);

        // RadioButtonValue aucun
        aucunAlignement = new RadioButtonValue("Aucun", new int[]{0}, new int[][] {valeurAlignement}, null);
        aucunAlignement.setSelected(true);
        alignement.add(aucunAlignement);
        groupAlignement.add(aucunAlignement);

        // RadioButtonValue horizontal
        RadioButtonValue horizontal = new RadioButtonValue("Horizontal", new int[]{1}, new int[][] {valeurAlignement}, null);
        alignement.add(horizontal);
        groupAlignement.add(horizontal);

        // RadioButtonValue vertical
        RadioButtonValue vertical = new RadioButtonValue("Vertical", new int[]{2}, new int[][] {valeurAlignement}, null);
        alignement.add(vertical);
        groupAlignement.add(vertical);

        // RadioButtonValue diagonal
        RadioButtonValue diagonal = new RadioButtonValue("Diagonal", new int[]{3}, new int[][] {valeurAlignement}, null);
        alignement.add(diagonal);
        groupAlignement.add(diagonal);
        JMenu circulaire = new JMenu("Circulaire");
        alignement.add(circulaire);

        // RadioButtonValue centre
        RadioButtonValue centre = new RadioButtonValue("Autour du centre du court", new int[]{4}, new int[][] {valeurAlignement}, null);
        circulaire.add(centre);
        groupAlignement.add(centre);

        // RadioButtonValue centre
        RadioButtonValue centreRect = new RadioButtonValue("Autour du centre du rectangle", new int[]{5}, new int[][] {valeurAlignement}, null);
        circulaire.add(centreRect);
        groupAlignement.add(centreRect);

        // RadioButtonValue inscrit
        RadioButtonValue inscrit = new RadioButtonValue("Inscrit au rectangle", new int[]{6}, new int[][] {valeurAlignement}, null);
        circulaire.add(inscrit);
        groupAlignement.add(inscrit);

        // JCheckBox uniforme
        uniforme = new JCheckBox("Uniforme");
        alignement.add(uniforme);

        // JMenu mouvement
        JMenu menuMouvement = new JMenu("Fct de mouvement");
        menuMouvement.setBounds(250, 0, 150, heightMenuBar);
        menuBar.add(menuMouvement);
        ButtonGroup groupMouvementGlobal = new ButtonGroup();
        ButtonGroup groupMouvementH = new ButtonGroup();
        ButtonGroup groupMouvementC = new ButtonGroup();
        // Valeurs de mouvement globale, horizontale et circulaire
        valeurMouvementGlobal = new int[1]; // 0 pour aucune, 1 pour non-global, 2 et 3 pour rotation centrale
        valeurMouvementH = new int[1];
        valeurMouvementC = new int[1];

        // RadioButtonValue aucuneFonction
        aucuneFonction = new RadioButtonValue("Aucune",
        new int[]{0, 0, 0}, new int[][] {valeurMouvementH, valeurMouvementC, valeurMouvementGlobal}, new ButtonGroup[]{groupMouvementH, groupMouvementC});
        aucuneFonction.setSelected(true);
        groupMouvementGlobal.add(aucuneFonction);
        menuMouvement.add(aucuneFonction);

        // JMenu traverseeH
        JMenu traverseeH = new JMenu("Traversée horizontale");
        menuMouvement.add(traverseeH);

        // RadioButtonValue traverséeGD
        RadioButtonValue traverseeGD = new RadioButtonValue("De gauche à droite",
        new int[]{1, 1}, new int[][] {valeurMouvementGlobal, valeurMouvementH}, new ButtonGroup[]{groupMouvementGlobal});
        groupMouvementH.add(traverseeGD);
        traverseeH.add(traverseeGD);

        // RadioButtonValue traverséeGD
        RadioButtonValue traverseeDG = new RadioButtonValue("De droite à gauche",
        new int[]{1, 2}, new int[][] {valeurMouvementGlobal, valeurMouvementH}, new ButtonGroup[]{groupMouvementGlobal});
        groupMouvementH.add(traverseeDG);
        traverseeH.add(traverseeDG);

        // JMenu fctCirculaire
        JMenu rotation = new JMenu("Rotation");
        menuMouvement.add(rotation);
        
        // RadioButtonValue rotationCentrale
        RadioButtonValue rotationCentrale = new RadioButtonValue("Autour du centre du court",
        new int[]{2}, new int[][] {valeurMouvementGlobal}, new ButtonGroup[]{groupMouvementH, groupMouvementC});
        groupMouvementGlobal.add(rotationCentrale);
        rotation.add(rotationCentrale);

        // RadioButtonValue rotationCentraleRect
        RadioButtonValue rotationCentraleRect = new RadioButtonValue("Autour du centre du rectangle",
        new int[]{1, 1}, new int[][] {valeurMouvementGlobal, valeurMouvementC}, new ButtonGroup[]{groupMouvementGlobal});
        aucuneFonction.setSelected(true);
        groupMouvementC.add(rotationCentraleRect);
        rotation.add(rotationCentraleRect);

        // RadioButtonValue rotationInscrite
        RadioButtonValue rotationInscrite = new RadioButtonValue("Suivant le cerlce inscrit au rectangle",
        new int[]{1, 3}, new int[][] {valeurMouvementGlobal, valeurMouvementC}, new ButtonGroup[]{groupMouvementGlobal});
        rotationInscrite.addActionListener(e -> inscrit.doClick());
        groupMouvementC.add(rotationInscrite);
        rotation.add(rotationInscrite);

        // JCheckbox sensAntiHoraire
        JCheckBox sensAntiHoraire = new JCheckBox("Sens anti-horaire");
        sensAntiHoraire.addItemListener(new ItemListener() {    
            public void itemStateChanged(ItemEvent e) {           
                if (e.getStateChange()==1) {
                    if (valeurMouvementC[0] != 0) valeurMouvementC[0]++;
                    if (valeurMouvementGlobal[0] == 2) valeurMouvementGlobal[0]++;
                } else {
                    if (valeurMouvementC[0] != 0) valeurMouvementC[0]--;
                    if (valeurMouvementGlobal[0] == 3) valeurMouvementGlobal[0]--;
                }
            }
            });   
        rotation.add(sensAntiHoraire);

        // JLabel labelSpeedPegs
        menuMouvement.addSeparator();
        JLabel labelSpeedPegs = new JLabel("Vitesse des pegs (px/s):");
        menuMouvement.add(labelSpeedPegs);

        // HashTabel labelTableSpeed
        Hashtable<Integer, JLabel> labelTableSpeed = new Hashtable<Integer, JLabel>();
        labelTableSpeed.put(50, new JLabel("50"));
        labelTableSpeed.put(150, new JLabel("150"));
        labelTableSpeed.put(250, new JLabel("250"));
        labelTableSpeed.put(350, new JLabel("350"));

        // JSlider speedPegs
        valeurVitesse = 100;
        sliderSpeedPegs = new JSlider(50, 350, 100);
        sliderSpeedPegs.setMinorTickSpacing(10);
        sliderSpeedPegs.setMajorTickSpacing(50);
        sliderSpeedPegs.setLabelTable(labelTableSpeed);
        sliderSpeedPegs.setPaintLabels(true);
        sliderSpeedPegs.setPaintTicks(true);
        sliderSpeedPegs.addChangeListener(e -> valeurVitesse = sliderSpeedPegs.getValue());
        menuMouvement.add(sliderSpeedPegs);

        // JPanel panelCasesPeg
        JPanel panelCasesPeg = new JPanel();
        panelCasesPeg.setLayout(null);
        panelCasesPeg.setBounds(courtWidth, heightMenuBar, width - courtWidth, courtHeight);
        add(panelCasesPeg);

        // case Peg bleu
        casePegBleu = new CasePeg(width-courtWidth, courtHeight * 1/4, 1);
        casePegBleu.setBounds(0, 0, width - courtWidth, courtHeight * 1/4);
        panelCasesPeg.add(casePegBleu);

        // case Peg Rouge
        casePegRouge = new CasePeg(width-courtWidth, courtHeight * 1/4, 2);
        casePegRouge.setBounds(0, courtHeight * 1/4, width - courtWidth, courtHeight * 1/4);
        panelCasesPeg.add(casePegRouge);

        // case Peg Violet
        casePegViolet = new CasePeg(width-courtWidth, courtHeight * 1/4, 3);
        casePegViolet.setBounds(0, courtHeight * 1/2, width - courtWidth, courtHeight * 1/4);
        panelCasesPeg.add(casePegViolet);

        // case peg Vert
        casePegVert = new CasePeg(width-courtWidth, courtHeight * 1/4, 4);
        casePegVert.setBounds(0, courtHeight * 3/4, width - courtWidth, courtHeight * 1/4);
        panelCasesPeg.add(casePegVert);

        // JPanel panelBoutons
        JPanel panelBoutons = new JPanel();
        int gap = (height - courtHeight - heightMenuBar)/4;
        panelBoutons.setBounds(0, courtHeight + heightMenuBar, width, height - courtHeight - heightMenuBar);
        panelBoutons.setLayout(null);
        add(panelBoutons);

        // slider peg selectionné
        sliderPegSelectionne = new JSlider(5, 60, 25);
        sliderPegSelectionne.setBorder(BorderFactory.createLineBorder(Color.BLACK));
        sliderPegSelectionne.setBounds(0, gap, width - courtWidth, largeurBouton);
        sliderPegSelectionne.addChangeListener(e -> {
            for (Pegs peg: pegsSelectionnes) {
                peg.setRadius(sliderPegSelectionne.getValue());
            }
            court.setPegs(court.clonePegs(niveauCree.getPegs()));
            court.repaint();
        });
        panelBoutons.add(sliderPegSelectionne);

        // BoutonCouleur bleu
        bleu = new BoutonCouleur(1);
        bleu.setLocation(width - courtWidth, gap);
        panelBoutons.add(bleu);

        // BoutonCouleur rouge
        rouge = new BoutonCouleur(2);
        rouge.setLocation(width - courtWidth + largeurBouton, gap);
        panelBoutons.add(rouge);

        // BoutonCouleur violet
        violet = new BoutonCouleur(3);
        violet.setLocation(width - courtWidth + 2*largeurBouton, gap);
        panelBoutons.add(violet);

        // BoutonCouleur vert
        vert = new BoutonCouleur(4);
        vert.setLocation(width - courtWidth + 3*largeurBouton, gap);
        panelBoutons.add(vert);

        // JButton croix
        croix = new BoutonPanel("Menu/croixRouge.png", largeurBouton, largeurBouton) ;
        croix.setBounds(width - courtWidth + 4*largeurBouton, gap, largeurBouton, largeurBouton);
        croix.addActionListener(e -> {
            for (Pegs peg : pegsSelectionnes) {
                niveauCree.getPegs().remove(peg);
            }
            pegsSelectionnes.clear();
            court.setPegs(court.clonePegs(niveauCree.getPegs()));
            court.repaint();
        });
        panelBoutons.add(croix);

        // Bouton pause
        JButton pause = new BoutonPanel("Menu/pause.png", largeurBouton, largeurBouton) ;
        pause.setBounds(courtWidth - 2*largeurBouton, gap, largeurBouton, largeurBouton);
        panelBoutons.add(pause);    
        pause.setEnabled(false);

        // Bouton resume
        JButton resume = new BoutonPanel("Menu/resume.png", largeurBouton, largeurBouton) ;
        resume.setBounds(courtWidth - largeurBouton, gap, largeurBouton, largeurBouton);
        resume.addActionListener(e -> {
            court.setEnPause(false);
            court.setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
            court.animate();
            resume.setEnabled(false);
            pause.setEnabled(true);
            caseActive.unclicked();
        });
        panelBoutons.add(resume);

        pause.addActionListener(e -> {
            court.setEnPause(true);
            // Remet en place les pegs originels.
            court.setPegs(court.clonePegs(niveauCree.getPegs()));
            court.getToucherPegs().clear();
            // Enlève les balles toujours sur le court
            for (Ball ball: court.getBalls()) {
                if (ball.isPresent()) ball.setPresent(false);
            }
            court.repaint();
            resume.setEnabled(true);
            pause.setEnabled(false);
            casePegBleu.mousePressed(null);
        });

        //JButton modif
        modif = new BoutonPanel("Menu/curseurMain.png", largeurBouton, largeurBouton) ;
        modif.setBounds(courtWidth - 3*largeurBouton, gap, largeurBouton, largeurBouton);
        modif.addActionListener(e -> {
            pause.doClick();
            enModif = true;
            caseActive.unclicked();
            court.setCursor(new Cursor(Cursor.HAND_CURSOR));
        });
        panelBoutons.add(modif);

        // Réglages par défaut
        casePegBleu.mousePressed(null);
        setFocusable(true);
        this.addKeyListener(new BoutonMenu.BoutonClavier(new BoutonMenu[]{}, ()-> controleur.launchMenu()));
        requestFocusInWindow() ;

    }

    public void boutonsModifActifs(boolean activer) {
        sliderPegSelectionne.setEnabled(activer);
        bleu.setEnabled(activer);
        rouge.setEnabled(activer);
        violet.setEnabled(activer);
        vert.setEnabled(activer);
        croix.setEnabled(activer);
    }

    public void reset() {
        niveauCree = new Niveau("enAttente");
        court.setNiveau(niveauCree);
        court.getPegs().clear();
        court.getToucherPegs().clear();
        court.repaint();
        casePegBleu.sliderRayonPeg.setValue(25);
        casePegRouge.sliderRayonPeg.setValue(25);
        casePegViolet.sliderRayonPeg.setValue(25);
        casePegVert.sliderRayonPeg.setValue(25);
        nomNiveau.setText(" Nom du niveau");
        uniforme.setSelected(false);
        campagne.setSelected(false);
        aucunAlignement.doClick();
        aucuneFonction.doClick();
        sliderSpeedPegs.setValue(100);
        sliderNbBallesInitial.setValue(10);
    }


    public class CasePeg extends JPanel implements MouseInputListener{

        int largeur, hauteur, couleur;
        Pegs peg; // Le peg représenté dans la case.
        Pegs modeleActuel; // Le peg utilisé en preview sur le court.
        JSlider sliderRayonPeg;

        public CasePeg(int largeur, int hauteur, int couleur) {
            this.largeur = largeur;
            this.hauteur = hauteur;
            this.couleur = couleur;
            peg = new Pegs(largeur/2, hauteur*3/4/2, 25, couleur);
            modeleActuel = new Pegs(-100, -100, peg.getRadius(), couleur);

            setLayout(null);
            sliderRayonPeg = new JSlider(5, 60, 25);
            sliderRayonPeg.setBounds(0, hauteur*3/4, largeur, hauteur*1/4);
            sliderRayonPeg.setBorder(BorderFactory.createLineBorder(Color.BLACK));
            sliderRayonPeg.addChangeListener(e -> {
                peg.setRadius(sliderRayonPeg.getValue());
                paint(this.getGraphics());
                modeleActuel.setRadius(sliderRayonPeg.getValue());
            });
            add(sliderRayonPeg);

            addMouseListener(this);
            addMouseMotionListener(this);
        }

        public void paint(Graphics g) {
            super.paint(g);
            Graphics2D g2d = (Graphics2D) g;
            g2d.drawImage(ImageImport.getImage(peg.getImageString()), (int) peg.getX()-peg.getRadius(), (int) peg.getY()-peg.getRadius(), peg.getDiametre(), peg.getDiametre(), this);
        }

        public void unclicked() {
            setBackground(UIManager.getColor("Panel.background")); // Rend au panel son background originel.
        }

        public void mousePressed(MouseEvent e) {
            if (caseActive != null) caseActive.unclicked();
            caseActive = this;
            enModif = false;
            boutonsModifActifs(false);
            court.setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
            setBackground(Color.LIGHT_GRAY);
        }

        public void mouseClicked(MouseEvent e) {}
        public void mouseReleased(MouseEvent e) {}
        public void mouseEntered(MouseEvent e) {}
        public void mouseExited(MouseEvent e) {}
        public void mouseDragged(MouseEvent e) {}
        public void mouseMoved(MouseEvent e) {}
    }

    public class BoutonPanel extends JButton{

        public BoutonPanel(String pathIcon, int width, int height){
            this.setIcon(new ImageIcon(ImageImport.getImage(pathIcon, width, height)));
            this.setBorderPainted(false); 
            this.setContentAreaFilled(false); 
            this.setFocusPainted(false); 
            this.setOpaque(false);
            this.setSize(width, height) ;
        }
    }

    public class BoutonCouleur extends JButton {

        int couleur;

        public BoutonCouleur(int couleur) {
            this.couleur = couleur;
            addActionListener(e -> {
                for (Pegs peg : pegsSelectionnes) {
                    peg.setCouleur(couleur);
                    peg.setImageString(Pegs.intColorToString(couleur));
                }
                court.setPegs(court.clonePegs(niveauCree.getPegs()));
                court.repaint();
            });
            Icon icon = new ImageIcon(ImageImport.getImage(Pegs.intColorToString(couleur), largeurBouton, largeurBouton));
            setBorderPainted(false); 
            setContentAreaFilled(false); 
            setFocusPainted(false); 
            setOpaque(false);
            setIcon(icon);  
            setSize(largeurBouton, largeurBouton);
        }
    }

    // Classe conçue pour les radioButton des menus alignement et mouvement.
    public class RadioButtonValue extends JRadioButtonMenuItem {
        int clickCount;

        // Constructeur prenant un tableau de valeurs et un tableau de tableaux contenant des variables
        // auxquelles affecter les valeurs. Le tableau de groupes correspond aux groupes qu'il
        // faut déselectionner lorsque le radioButton est selectionné.
        public RadioButtonValue(String text, int[] values, int[][] dest, ButtonGroup[] groups) {
            super(text);
            addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    for (int i = 0; i < values.length; i++) {
                        dest[i][0] = values[i];
                    }
                    if (modif != null && !enModif) modif.doClick();
                    if (groups != null) {
                        for (int i = 0; i < groups.length; i++) {
                            if (groups[i] != null) groups[i].clearSelection();
                        }
                    }
                };
            });
        }
    }
}
