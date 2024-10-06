package Vue.Menu;

import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.image.BufferedImage;

import javax.swing.ImageIcon;
import javax.swing.JButton;

import Vue.ImageImport;

public class BoutonMenu extends JButton {
    
    int width, height;
    ImageIcon imageIconNormal;
    ImageIcon imageIconOnHover;
    MouseListener ml;

    public BoutonMenu(String texteImage, int width, int height){
        this.width = width;
        this.height = height;
        imageIconNormal = getEditedImageIcon(texteImage, width, height, true);
        imageIconOnHover = getEditedImageIcon(texteImage, width, height, false);
        setIcon(imageIconNormal);
        ml = (MouseListener) new MouseAdapter() {
            public void mouseEntered(MouseEvent evt) {setIcon(imageIconOnHover);}
            public void mouseExited(MouseEvent evt) {setIcon(imageIconNormal);}
            public void mousePressed(MouseEvent evt) {setIcon(imageIconNormal);}
        } ;
        addMouseListener(ml);
        // Parametrages du bouton
        setBorderPainted(false); 
        setContentAreaFilled(false); 
        setFocusPainted(false); 
        setOpaque(false);
        setSize(width, height);
    }
    
    public MouseListener getMouseListener() {return ml;}

    public void setCouleur(boolean jaune){
        if (jaune) setIcon(imageIconOnHover) ;
        else setIcon(imageIconNormal);
    }

    public ImageIcon getEditedImageIcon (String texte, int width, int height, boolean normal) {
        BufferedImage buffImg;
        if (normal) buffImg = ImageImport.getImage("Menu/planche_blanche.png", width, height);
        else buffImg = ImageImport.getImage("Menu/planche_jaune.png", width, height);
        Graphics g = buffImg.getGraphics();
        Font rightFont = rightFont(texte, g);
        FontMetrics metrics = g.getFontMetrics(rightFont);
        g.setFont(rightFont);
        if (normal) g.setColor(Color.WHITE);
        else g.setColor(Color.YELLOW);
        g.drawString(texte, width/2 - metrics.stringWidth(texte)/2, height/2 + metrics.getAscent()/2);
        return new ImageIcon(buffImg);
    }

    // Retourne une font dont la taille est adaptée aux dimensions du bouton.
    public Font rightFont (String texte, Graphics g) {
        Font rightF = ImageImport.cartoon.deriveFont(1000f); // Très grande taille de police par défault
        FontMetrics metrics = g.getFontMetrics(rightF);
        int fontSize = rightF.getSize();

        // Rétrécit la taille de la font si la hauteur du texte sera trop grande.
        int textHeight = metrics.getAscent();
        int textHeightMax = height * 1/2;
        if (textHeight > textHeightMax) {
            double heightRatio = (double) textHeightMax / (double) textHeight;
            rightF = rightF.deriveFont((float) Math.floor(fontSize * heightRatio));
            fontSize = rightF.getSize();
            metrics = g.getFontMetrics(rightF);
        }

        // Rétrécit la taille de la font si la largeur du texte sera trop grande.
        int textWidth = metrics.stringWidth(texte);
        int textWidthMax = width * 5/6;
        if (textWidth > textWidthMax) {
            double widthRatio = (double) textWidthMax / (double) textWidth;
            rightF = rightF.deriveFont((float) Math.floor(fontSize * widthRatio));
            fontSize = rightF.getSize();
            metrics = g.getFontMetrics(rightF);
        }

        return rightF;
    }

    public static class BoutonClavier implements KeyListener{
        private BoutonMenu[] allBouton ;
        private int selecteur ;
        private int nbrBoutton ;
        private Action action ;

        public interface Action {
            void perf() ;
        }

        public BoutonClavier(BoutonMenu[] allBouton, Action actionToucheEchap){ 
            this.action = actionToucheEchap ;
            this.allBouton = allBouton ;
            nbrBoutton = allBouton.length ;
            resetSelecteur();
        }


        public void keyTyped(KeyEvent e) {
        }

        private BoutonMenu getButton(int i) {
            selecteur = (selecteur + nbrBoutton) % nbrBoutton;
            return allBouton[i] ;
        }
        private void resetSelecteur(){selecteur =-1 ;}

        private void iluminateButton() {
            selecteur = (selecteur + nbrBoutton) % nbrBoutton;
            for (int i = 0; i < nbrBoutton; i++) {
                if (i == selecteur)
                    getButton(i).setCouleur(true);
                else
                    getButton(i).setCouleur(false);
            }
        }

        @Override
        public void keyPressed(KeyEvent e) {
            switch (e.getKeyCode()) {
                case (KeyEvent.VK_ESCAPE):
                case (KeyEvent.VK_CONTROL):
                    action.perf() ;
                    break;
                case (KeyEvent.VK_DOWN):
                    if (selecteur == -1) selecteur = -2 ; //si reset
                    selecteur++;
                    iluminateButton();
                    break;
                case (KeyEvent.VK_UP):
                    if (selecteur == -1) selecteur = 1 ; //si reset
                    selecteur--;
                    iluminateButton();
                    break;
                case (KeyEvent.VK_ENTER):
                    if (selecteur != -1) getButton(selecteur).doClick();
                    break;

                default:
                    break;
            }
        }

        @Override
        public void keyReleased(KeyEvent e) {
        }
    }
}
