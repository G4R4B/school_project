package Vue;

import Vue.Menu.BoutonMenu;
import java.awt.Color;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.image.BufferedImage;

import javax.swing.*;

import Modele.Ball;
import Modele.Niveau;

public class GameView extends JPanel {

    public Controleur controleur;
    private int width;
    private int heigth;

    Niveau niveau;

    // Court
    public Court court;
    private int courtWidth;
    private int courtHeight;
    private static int tailleligne = 4;

    JButton btnRetour;

    // menu pause
    JeuEnpause jeuEnpause;

    public GameView(Controleur c, String nomNiveau) {

        this.controleur = c;

        width = controleur.getWidth();
        while ((width /12) < tailleligne * (Ball.ballRadius * 2 + 10)+ 30 + Ball.ballRadius) {
            tailleligne--;
        if (tailleligne == 1) {break;}
        }
        heigth = controleur.getHeight();
        setSize(width, heigth);
        setLayout(null);
        setVisible(true);
        setBackground(Color.BLACK);

        courtWidth = width*5/6;
        courtHeight = heigth*5/6;


        // Affectation du niveau
        if (nomNiveau == null || nomNiveau.equals(""))
            niveau = new Niveau(nomNiveau);
        else if (nomNiveau.toLowerCase().equals("aleatoire"))
            niveau = Niveau.NiveauAleatoire(courtWidth, courtHeight, 20);
        else
            niveau = Niveau.importPegles(nomNiveau, courtWidth, courtHeight);

        jeuEnpause = new JeuEnpause();

        // Court
        court = new Court(courtWidth, courtHeight, niveau, c);
        court.setBorder(BorderFactory.createLineBorder(Color.BLACK));
        court.setBounds((width - courtWidth) / 2, (heigth - courtHeight) / 2, courtWidth, courtHeight);
        court.setVisible(true);
        add(court);

        // JButton bouton retour
        btnRetour = new BoutonMenu("Pause", tailleligne * (Ball.ballRadius * 2 + 10), 50);
        btnRetour.setLocation(35 - Ball.ballRadius, 20);
        btnRetour.setVisible(true);
        btnRetour.addActionListener(e -> launchMenuPause(true));
        add(btnRetour);

        // Background
        Background background = new Background(court, heigth, width);
        background.setBounds(0, 0, width, heigth);
        background.setOpaque(false);
        add(background);

        
    }

    public void launchMenuPause(boolean visible) {
        jeuEnpause.setVisible(visible);
        jeuEnpause.menuEnpause.setVisible(visible);
        court.setEnPause(visible);
        btnRetour.setVisible(!visible);
        btnRetour.setEnabled(!visible);
        jeuEnpause.repaint();
        if (!visible) {
            court.requestFocusInWindow();
            court.animate();
        } else {
            jeuEnpause.menuEnpause.requestFocusInWindow();
        }
    }

    class JeuEnpause extends JPanel {
        MenuEnpause menuEnpause;

        JeuEnpause() {
            setLayout(null);
            menuEnpause = new MenuEnpause();
            setSize(width, heigth);
            add(menuEnpause);
            setOpaque(true);
            setVisible(false);
            setLocation(0, 0);
            GameView.this.add(this);
            setBackground(new Color(0, 0, 0, 150));

        }

        class MenuEnpause extends JPanel {
            BufferedImage arrierePlan;
            BoutonMenu resume;
            BoutonMenu restart;
            BoutonMenu quit;

            MenuEnpause() {
                // mettre le jeux en pause
                setLayout(null);
                setSize(courtWidth / 2, courtHeight);
                setLocation(width / 2 - this.getWidth() / 2, heigth / 2 - this.getHeight() / 2);
                setOpaque(false);
                setVisible(true);

                // definir image de fond :
                arrierePlan = ImageImport.getImage("Gameview/ResumeScreen.png", courtWidth / 2, courtHeight);

                // ajout des boutons

                int y = (this.getHeight() * 200) / 876;

                resume = new BoutonMenu("Reprendre", (this.getWidth()) / 2, (50*courtHeight)/520);
                resume.setLocation(this.getWidth() / 2 - resume.getWidth() / 2, y- resume.getHeight()/2);
                resume.setVisible(true);
                resume.addActionListener(e -> {
                    launchMenuPause(false);
                });
                add(resume);

                restart = new BoutonMenu("Recommencer", (this.getWidth()) / 2, (50*courtHeight)/520);
                restart.setLocation(this.getWidth() / 2 - restart.getWidth() / 2, y * 2 - resume.getHeight()/2);
                restart.setVisible(true);
                restart.addActionListener(e -> {
                    controleur.launchGameview(niveau.getDossier());
                });
                add(restart);

                quit = new BoutonMenu("Quitter", (this.getWidth()) / 2, (50*courtHeight)/520);
                quit.setLocation(this.getWidth() / 2 - quit.getWidth() / 2, y * 3 - resume.getHeight()/2);
                quit.setVisible(true);
                quit.addActionListener(e -> controleur.launchMenu());
                add(quit);

                setFocusable(true);
                addKeyListener(new BoutonMenu.BoutonClavier(new BoutonMenu[]{resume, restart, quit}, ()->launchMenuPause(false)) );
            }
            public void Textentete(String texteEntete,  Graphics g){
                g.setFont(ImageImport.rightSizeArcade(texteEntete, (this.getWidth() * 573) / 781));
                g.setColor(Color.WHITE);
                FontMetrics fm = g.getFontMetrics(g.getFont()) ;
                int offsetX = ((this.getWidth() * 573) / 781) - fm.stringWidth(texteEntete) ;
                int offsetY = fm.getAscent()/2 ;
                g.drawString(texteEntete, (this.getWidth() * 104) / 781 +offsetX, (this.getHeight() * 45) / 876 + offsetY);
            }

            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                g.drawImage(arrierePlan, 0, 0, this);
                Textentete("Niveau " + niveau.getNom() + " !", g);
            }

        }

    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return width;
    }

    public int getCourtWidth() {
        return courtWidth;
    }

    public int getCourtHeight() {
        return courtHeight;
    }

    public static int getTailleligne() {
        return tailleligne;
    }


}
