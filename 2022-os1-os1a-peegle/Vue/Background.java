package Vue;

import javax.swing.JPanel;

import Modele.Ball;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Toolkit;
import java.awt.image.BufferedImage;
import java.awt.image.BufferedImageOp;
import java.awt.image.ConvolveOp;
import java.awt.image.Kernel;

public class Background extends JPanel {
  private static String pathBackGround = "Gameview/arbre.jpg";
  private static int selecteurBackground = 0 ; 
  
  
  private BufferedImage backgroundImage;
  
  private Font newFont = ImageImport.arcade;
  private Court court;
  
  // score
  private int longeur, largeur;
  private int midBordureCourtX, midBordureCourtY;
  private BufferedImage score;
  private int width;
  private int heigth;
  private int scoreMax;
  private int taille1Etoille;
  
  // balle
  private BufferedImage ball;
  private boolean GameOver = false;
  private BufferedImage balleRestImage;
  
  public static int getSelecteurBackground() {
    return selecteurBackground;
  }

  public static void setSelecteurBackground(int selecteurBackground) {
    Background.selecteurBackground = selecteurBackground;
  }
  public static void setPathBackGround(String pathBackGround) {
    Background.pathBackGround = pathBackGround;
  }

  // Some code to initialize the background image.
  // Here, we use the constructor to load the image. This
  // can vary depending on the use case of the panel.
  public Background(Court court, int h, int w) {
    heigth = h;
    width = w;
    this.court = court;
    this.court.setBackground(this);
    this.scoreMax = court.getScoreMaxBackground();
    Dimension size = Toolkit.getDefaultToolkit().getScreenSize();
    backgroundImage = ImageImport.getImage(pathBackGround, size.width, size.height);

    for (int i = 0; i < 10; i++) {
      float[] blurKernel = { 1 / 16f, 2 / 16f, 1 / 16f, 2 / 16f, 4 / 16f, 2 / 16f, 1 / 16f, 2 / 16f, 1 / 16f };
      BufferedImageOp blur = new ConvolveOp(new Kernel(3, 3, blurKernel));
      backgroundImage = blur.filter(backgroundImage, null);

    }

    int bordureDroiteLargeur = (width - court.getWidth()) / 2 + court.getWidth();
    int bordureDroiteHauteur = (heigth - court.getHeight()) / 2 + court.getHeight();

    midBordureCourtX = bordureDroiteLargeur + 30;
    midBordureCourtY = bordureDroiteHauteur - court.getHeight() + 50;
    largeur = (width - 30) - midBordureCourtX;
    longeur = (bordureDroiteHauteur - 50) - midBordureCourtY;
    ball = ImageImport.getImage("Ball/ball.png", 50, 50);

    ball = court.getBall();

    taille1Etoille = largeur / 5;
  }

  public void paintComponent(Graphics g) {
    super.paintComponent(g);

    Graphics2D g2d = (Graphics2D) g;

    // Draw the background image.
    g2d.drawImage(backgroundImage, null, 3, 3);
    if (GameOver) {
      return;
    }
    if (newFont != null) {
      g.setFont(newFont.deriveFont(20f));
    }

    // score
    g.drawRect(midBordureCourtX, midBordureCourtY, largeur, longeur);
    score = getEditedImage("SCORE :", String.valueOf(court.getScore()), largeur, 60);
    g.drawImage(score, midBordureCourtX, midBordureCourtY - score.getHeight() - 5, this);
    int scorebarre = court.getScore();
    if (scorebarre > scoreMax)
      scorebarre = scoreMax;
    int score = 0;
    if (scoreMax != 0)
      score = scorebarre * longeur / scoreMax;
    int point = midBordureCourtY + longeur - score;

    if (score <= longeur * 1 / 3) {
      g.setColor(Color.RED);
    } else if (score <= longeur * 2 / 3) {
      g.setColor(Color.ORANGE);
    } else {
      g.setColor(Color.GREEN);
    }
    g.fillRect(midBordureCourtX + 1, point, largeur - 1, (midBordureCourtY + longeur) - point);

    // etoile de score
    ShowStars(g);

    // balle
    int ligne = 0;
    int pointDeDepartX = 40;
    int pointDeDepartY = court.getY() + court.getHeight() - 45;
    int XBall = pointDeDepartX - Ball.ballRadius;
    
    int tailleligne = GameView.getTailleligne();
    for (int i = 0; i < court.getNbDeBall(); i++) {
      if (i % tailleligne == 0)
        ligne++;
      if (pointDeDepartY - (ligne) * (Ball.ballRadius * 2 + 10) < 110) { // affiche que le nombre necessaire à l'écran
        ligne--;
        break;
      }
      g.drawImage(ball, XBall + i % tailleligne * (Ball.ballRadius * 2 + 10), pointDeDepartY - ligne * (Ball.ballRadius * 2 + 10),
          this);
    }
    g.setColor(Color.WHITE);
    g.drawRect(XBall - 10, pointDeDepartY - (ligne) * (Ball.ballRadius * 2 + 10) - 10,
    tailleligne * (Ball.ballRadius * 2 + 10) + 10, ligne * (Ball.ballRadius * 2 + 10));

    // annonceur nombre de balles restantes
    balleRestImage = getEditedImage(court.getNbDeBall() <= 1 ? "Balle :" : "Balles :", "X" + court.getNbDeBall(),
    tailleligne * (Ball.ballRadius * 2 + 10), 60);
    g.drawImage(balleRestImage, XBall - 5, pointDeDepartY, court);

  }

  private void ShowStars(Graphics g) {
    boolean colore = court.getScore() >= court.getNiveau().getScore1Etoiles();
    g.drawImage(getImageEtoile(colore), midBordureCourtX + (largeur - 1 * taille1Etoille) / 2,
        midBordureCourtY + (longeur * 3) / 4, this);

    colore = court.getScore() >= court.getNiveau().getScore2Etoiles();
    g.drawImage(getImageEtoile(colore), midBordureCourtX + (largeur - 2 * taille1Etoille) / 2,
        midBordureCourtY + (longeur * 2) / 4, this);
    g.drawImage(getImageEtoile(colore), midBordureCourtX + (largeur - 2 * taille1Etoille) / 2 + taille1Etoille * 1,
        midBordureCourtY + (longeur * 2) / 4, this);

    colore = court.getScore() >= court.getNiveau().getScore3Etoiles();
    g.drawImage(getImageEtoile(colore), midBordureCourtX + (largeur - 3 * taille1Etoille) / 2,
        midBordureCourtY + (longeur * 1) / 4, this);
    g.drawImage(getImageEtoile(colore), midBordureCourtX + (largeur - 3 * taille1Etoille) / 2 + taille1Etoille * 1,
        midBordureCourtY + (longeur * 1) / 4, this);
    g.drawImage(getImageEtoile(colore), midBordureCourtX + (largeur - 3 * taille1Etoille) / 2 + taille1Etoille * 2,
        midBordureCourtY + (longeur * 1) / 4, this);
  }

  private BufferedImage getImageEtoile(boolean colore) {
    if (colore)
      return ImageImport.getImage("Gameview/etoilePleine.png", taille1Etoille, taille1Etoille);
    else
      return ImageImport.getImage("Gameview/etoileVide.png", taille1Etoille, taille1Etoille);
  }

  public BufferedImage getEditedImage(String ligne1, String ligne2, int width, int height) {
    BufferedImage buffImg = ImageImport.getImage("Menu/planche_blanche.png", width, height);
    Graphics g = buffImg.getGraphics();
    // premiere ligne
    Font rightFont = rightFont(ligne1, g, width, height / 2);
    FontMetrics metrics = g.getFontMetrics(rightFont);
    g.setFont(rightFont);
    g.setColor(Color.WHITE);
    g.drawString(ligne1, width / 2 - metrics.stringWidth(ligne1) / 2, height / 4 + metrics.getAscent() / 2);

    // deuxieme ligne
    rightFont = rightFont(ligne2, g, width, height / 2);
    metrics = g.getFontMetrics(rightFont);
    g.setFont(rightFont);
    g.setColor(Color.YELLOW);
    g.drawString(ligne2, width / 2 - metrics.stringWidth(ligne2) / 2, (3 * height) / 4);

    return buffImg;
  }

  // Retourne une font dont la taille est adaptée aux dimensions de l'image.
  public Font rightFont(String texte, Graphics g, int width, int height) {
    Font rightF = ImageImport.cartoon.deriveFont(1000f); // Très grande taille de police par défault
    FontMetrics metrics = g.getFontMetrics(rightF);
    int fontSize = rightF.getSize();

    // Rétrécit la taille de la font si la hauteur du texte sera trop grande.
    int textHeight = metrics.getAscent();
    int textHeightMax = height * 1 / 2;
    if (textHeight > textHeightMax) {
      double heightRatio = (double) textHeightMax / (double) textHeight;
      rightF = rightF.deriveFont((float) Math.floor(fontSize * heightRatio));
      fontSize = rightF.getSize();
      metrics = g.getFontMetrics(rightF);
    }

    // Rétrécit la taille de la font si la largeur du texte sera trop grande.
    int textWidth = metrics.stringWidth(texte);
    int textWidthMax = width * 5 / 6;
    if (textWidth > textWidthMax) {
      double widthRatio = (double) textWidthMax / (double) textWidth;
      rightF = rightF.deriveFont((float) Math.floor(fontSize * widthRatio));
      fontSize = rightF.getSize();
      metrics = g.getFontMetrics(rightF);
    }

    return rightF;
  }

  public void setOver(boolean gameOver) {
    GameOver = gameOver;

  }
}