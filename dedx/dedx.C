#include "TH1F.h"
#include "TMath.h"
#include "TLorentzVector.h"


Int_t NEVENTS=100000;


//---------------------------------------------------------------

Double_t langaufun(Double_t *x, Double_t *par) {

   //Fit parameters:
   //par[0]=Width (scale) parameter of Landau density
   //par[1]=Most Probable (MP, location) parameter of Landau density
   //par[2]=Total area (integral -inf to inf, normalization constant)
   //par[3]=Width (sigma) of convoluted Gaussian function
   //
   //In the Landau distribution (represented by the CERNLIB approximation),
   //the maximum is located at x=-0.22278298 with the location parameter=0.
   //This shift is corrected within this function, so that the actual
   //maximum is identical to the MP parameter.

   // Numeric constants
   Double_t invsq2pi = 0.3989422804014;   // (2 pi)^(-1/2)
   Double_t mpshift  = -0.22278298;       // Landau maximum location

   // Control constants
   Double_t np = 100.0;      // number of convolution steps
   Double_t sc =   5.0;      // convolution extends to +-sc Gaussian sigmas

   // Variables
   Double_t xx;
   Double_t mpc;
   Double_t fland;
   Double_t sum = 0.0;
   Double_t xlow,xupp;
   Double_t step;
   Double_t i;

   // MP shift correction
   mpc = par[1] - mpshift * par[0];

   // Range of convolution integral
   xlow = x[0] - sc * par[3];
   xupp = x[0] + sc * par[3];

   step = (xupp-xlow) / np;

   // Convolution integral of Landau and Gaussian by sum
   for(i=1.0; i<=np/2; i++) {

      xx = xlow + (i-.5) * step;
      fland = TMath::Landau(xx,mpc,par[0]) / par[0];
      sum += fland * TMath::Gaus(x[0],xx,par[3]);

      xx = xupp - (i-.5) * step;
      fland = TMath::Landau(xx,mpc,par[0]) / par[0];
      sum += fland * TMath::Gaus(x[0],xx,par[3]);
   }

   return (par[2] * step * sum * invsq2pi / par[3]);
}

//---------------------------------------------------------------

// formula Taken from Leo (2.30) pg. 26
Double_t deltaf(double c0, double a, double m, double x0, double x1, double beta, double gamma)
{
   Double_t x= TMath::Log10(beta*gamma);
   Double_t delta = 0.;

   cout<<x<<","<<x0<<","<<x1<<","<<endl;

   if (x < x0)
       delta = 0.;
   if (x >= x0 && x< x1)
       delta = 4.6052*x - c0 + a*TMath::Power(x1 - x,m);
   if  (x> x1)
       delta = 4.6052*x - c0;

   return delta;
}

//---------------------------------------------------------------

Double_t Chi(double beta, double gamma, double charge, double x, double A, double Z, double rho)
{
  Double_t kappa = 2*0.1535*TMath::Abs(charge)*TMath::Abs(charge)*Z*rho*x/(A*beta*beta); //energy loss in MeV
  Double_t chi = 0.5*kappa;
  return chi;
}

//---------------------------------------------------------------

Double_t deltaP(double beta, double gamma, double charge, double x, double A, double Z, double rho, double I, double c0, double a, double m, double x0, double x1)
{
  Double_t chi = Chi(beta, gamma, charge, x, A, Z, rho);
  Double_t me = 0.510998; // electron mass in MeV, need
  I *= 1e-6; // convert I in MeV
  Double_t Wmax = 2*me*beta*beta*gamma*gamma; // this is not valid for electrons
  Double_t delta = deltaf(c0, a, m, x0, x1, beta, gamma);


  //Double_t DeDx= chi*( 2*TMath::Log(Wmax/I) - 2*beta*beta - delta);
  Double_t DeDx = 2*chi*( TMath::Log(Wmax/I) - beta*beta - delta/2);
  Double_t dP = chi*( TMath::Log(Wmax/I) + TMath::Log(chi/I) + 0.2 - beta*beta - delta);

        cout<<"    Wmax: "<<Wmax<<", Chi: "<<chi<<", delta: "<<delta<<", DeDx: "<<DeDx<<", DeltaP: "<<dP<<endl;

  return dP;
}

//---------------------------------------------------------------

Double_t truncMean(std::vector<Double_t> elosses, Double_t truncFrac)
{
     Int_t new_size = Int_t( elosses.size() * (1 - truncFrac));

     // remove outliers and re-compute mean
     elosses.resize(new_size);
     return accumulate( elosses.begin(), elosses.end(), 0.0)/elosses.size();
}
//------------------------------------------------------------------------------

void dedx()
{

  TH1F *hEnergyLoss1  = new TH1F("energy_loss1", "energy_loss1", 500, 0.0, 5.0);
  TH1F *hEnergyLoss2 = new TH1F("energy_loss2", "energy_loss2", 500, 0.0, 5.0);
  TH1F *hEnergyLoss3 = new TH1F("energy_loss3", "energy_loss3", 500, 0.0, 5.0);
  TH1F *hEnergyLoss4 = new TH1F("energy_loss4", "energy_loss4", 500, 0.0, 5.0);

  //mpv is the predicted <dEdx> from Bethe-Bloch
  Double_t mpv = 1.2;

  TLorentzVector pvec;

  //calculate mpv energy loss for pion in Silicon
  //Double_t mass = 0.139570; //139 MeV
  Double_t mass = 0.10565839; //139 MeV

  Double_t energy = 10.+mass;
  Double_t p = TMath::Sqrt(energy*energy - mass*mass);
  Double_t charge = 1;

  pvec.SetPtEtaPhiM(p,0.,0.,mass);
  Double_t beta = pvec.Beta();
  Double_t gamma = pvec.Gamma();
  mass = pvec.M();

  TLorentzVector pvec2;
  //calculate mpv energy loss for pion in Silicon
  //Double_t mass = 0.139570; //139 MeV
  Double_t mass2 = 100; //139 MeV

  Double_t energy2 = 50.+mass2;
  Double_t p2 = TMath::Sqrt(energy2*energy2 - mass2*mass2);
  Double_t charge2 = 1;

  pvec2.SetPtEtaPhiM(p2,0.,0.,mass2);
  Double_t beta2 = pvec2.Beta();
  Double_t gamma2 = pvec2.Gamma();
  mass2 = pvec2.M();


  // print particle properties
   cout<<"E: "<<pvec.E()<<", P: "<<pvec.P()<<", Pt: "<<pvec.Pt()<<", M: "<<pvec.M()<<", Beta: "<< pvec.Beta()<<", Gamma: "<<pvec.Gamma() <<", Charge: "<<charge<<endl;
  // print particle properties
   cout<<"E2: "<<pvec2.E()<<", P2: "<<pvec2.P()<<", Pt2: "<<pvec2.Pt()<<", M2: "<<pvec2.M()<<", Beta2: "<< pvec2.Beta()<<", Gamma2: "<<pvec2.Gamma() <<", Charge2: "<<charge2<<endl;

/*
Index =   14:  silicon (Si)
     Absorber with Z =  14,  A = 28.0855(3), density = 2.329 (revised)
 Sternheimer coef:  a     k=m_s   x_0    x_1    I[eV]   Cbar  delta0
                 0.1492  3.2546  0.2015  2.8716  173.0  4.4355 0.14
*/


  // --   silicon properties ---
  //------------------------------

  // generic properties
  Double_t Z      = 14.;
  Double_t A      = 28.0855; // in g/mol
  Double_t rho    = 2.329; // in g/cm3

  // for density correction calculations
  Double_t a      = 0.1492;
  Double_t m      = 3.2546;
  Double_t x0     = 0.2015;
  Double_t x1     = 2.8716;
  Double_t I      = 173.0; // mean excitation potential in (eV)
  Double_t c0     = 4.4355;

  /*

     Absorber with Z =  18,  A = 39.948(1), density = $ 1.662 \times10^{- 3}$
 Sternheimer coef:  a     k=m_s   x_0    x_1    I[eV]   Cbar  delta0
                 0.1971  2.9618  1.7635  4.4855  188.0 11.9480 0.00


  // --  argon gas properties ---
  //------------------------------

  // generic properties
  Double_t Z      = 18;
  Double_t A      = 39.948;
  Double_t rho    = 1.662e-3;

  // for density cor
  Double_t a      = 0.1971;
  Double_t m      = 2.9618;
  Double_t x0     = 1.7635;
  Double_t x1     = 4.4855;
  Double_t I      = 188.0;
  Double_t c0     = 11.9480;

*/

  // how much matter are we traversing in cm

  Double_t eff = 0.7; // 1.7 mm in Silicon


  // one measurement in 1 cm
  Double_t x = 0.1; // in cm

  // or 100 measurements in 100 um
  Double_t x2 = 0.01; // in cm

  int nhits = int(x/x2);

  //cout<<nhits<<endl;
  //cout<<beta<<","<<gamma<<","<<endl;

  Double_t chi = Chi(beta, gamma, charge, x2, A, Z, rho);
  Double_t DeltaP = deltaP(beta, gamma, charge, x2, A, Z, rho, I, c0, a, m, x0, x1);

  float dx = x2;
  cout<<"Nhits: "<<nhits<<", dx: "<<dx<<", Charge: "<<charge<<", Beta: "<< beta<<", Gamma: "<<gamma<<endl;

  Double_t chi2 = Chi(beta2, gamma2, charge2, x2, A, Z, rho);
  Double_t DeltaP2 = deltaP(beta2, gamma2, charge2, x2, A, Z, rho, I, c0, a, m, x0, x1);

  // formula (33.12) from http://pdg.lbl.gov/2019/reviews/rpp2018-rev-passage-particles-matter.pdf
  // x = 7.405e+00;
  // beta = 9.903e-01;
  // gamma =  7.199e+00;
  // charge = 1.000e+00;

  /*
  TF1 *flangaus = new TF1("langaus",langaufun,0., 20.,4);
  Double_t sv[4];
  sv[0]=chi;
  sv[1]=DeltaP;
  sv[2]=1.0;

  // additional gaussian smearing parameter
  // first pixel layer: sigma = 0.7
  // >= second pixel layer: sigma = 0.4

  //sv[3]=0.7;
  sv[3]=0.4;

  flangaus->SetParameters(sv);
  flangaus->SetParNames("Width","MP","Area","GSigma");

  //flangaus->Draw();
  */


  // event loop
  //Double_t sigma = 0.15;
  Double_t sigma = 0.4;  // 0.4 MeV/cm

  for (int i=0; i<NEVENTS; i++)
  {

     //Double_t eloss = gRandom->Landau(DeltaP2,chi2); // this is the total energy loss in MeV
     //Double_t eloss2 = gRandom->Gaus(eloss,sigma*x2);

     //Double_t eloss1 = gRandom->Uniform();

     //hEnergyLoss->Fill(eloss/x2);
     //hEnergyLoss2->Fill(eloss2/x2);

     std::vector<Double_t> elosses;
     std::vector<Double_t> elosses_smear;
     std::vector<Double_t> elosses2;
     std::vector<Double_t> elosses2_smear;

     for (int j=0; j<nhits; j++){

       Double_t eloss         = gRandom->Landau(DeltaP,chi);
       Double_t eloss_smear   = gRandom->Gaus(eloss,sigma*x2);

       Double_t eloss2        = gRandom->Landau(DeltaP2,chi2);
       Double_t eloss2_smear  = gRandom->Gaus(eloss2,sigma*x2);

       //cout<<eloss<<","<<eloss2<<endl;

       elosses.push_back(eloss);
       elosses2.push_back(eloss2);

       elosses_smear.push_back(eloss_smear);
       elosses2_smear.push_back(eloss2_smear);

     }

     // sort vector of energy losses from highest to lowest
     //std::sort (elosses.begin(), elosses.end(), greater<Double_t>());
     std::sort (elosses.begin(), elosses.end());
     std::sort (elosses2.begin(), elosses2.end());

     std::sort (elosses_smear.begin(), elosses_smear.end());
     std::sort (elosses2_smear.begin(), elosses2_smear.end());


     //cout << "--------------------------"<< endl;

     /*
     for (int j=0; j<nhits; j++){
       cout<< elosses.at(j)<<" , "<< elosses2.at(j)<<endl;
     }
     */

     Double_t fTruncFrac;

     /*
     fTruncFrac  = 0.1;
     Double_t eloss_mean2 =  truncMean(elosses, fTruncFrac);
     hEnergyLoss2->Fill(eloss_mean2/x2);

     fTruncFrac  = 0.33;
     Double_t eloss_mean3 =  truncMean(elosses, fTruncFrac);
     hEnergyLoss3->Fill(eloss_mean3/x2);
     */

     fTruncFrac  = 0.5;

     Double_t eloss_mean =  truncMean(elosses, fTruncFrac);
     hEnergyLoss1->Fill(eloss_mean/x2);

     Double_t eloss_mean2 =  truncMean(elosses2, fTruncFrac);
     hEnergyLoss2->Fill(eloss_mean2/x2);

     Double_t eloss_smear_mean =  truncMean(elosses_smear, fTruncFrac);
     hEnergyLoss3->Fill(eloss_smear_mean/x2);

     Double_t eloss_smear_mean2 =  truncMean(elosses2_smear, fTruncFrac);
     hEnergyLoss4->Fill(eloss_smear_mean2/x2);



     //Double_t eloss2 = gRandom->Landau(DeltaP2,chi2); // this is the total energy loss in MeV
     //Double_t eloss = gRandom->Uniform();

     //hEnergyLoss2->Fill(eloss2/x2);

     //Double_t eloss2 = flangaus->GetRandom(); // this is the total energy loss in MeV
     //hEnergyLoss2->Fill(eloss2);

     //cout<<eloss<<endl;

     //Double_t eloss3 = gRandom->Gaus(eloss1,sigma*eloss1);
      // Double_t eloss3 = gRandom->Gaus(eloss1,0.01);

     //hEnergyLoss3->Fill(eloss3);

     //Double_t eloss4 = gRandom->Gaus(eloss2,0.4);
     //Double_t eloss4 = gRandom->Gaus(eloss2,0.01);

     //Double_t eloss4 = gRandom->Gaus(eloss2,sigma*eloss2);
     //hEnergyLoss4->Fill(eloss4/x2);

  }

  hEnergyLoss1->SetLineWidth(2);
  hEnergyLoss1->SetLineColor(kOrange+2);
  hEnergyLoss1->DrawNormalized("");


  hEnergyLoss2->SetLineWidth(2);
  hEnergyLoss2->SetLineColor(kGreen+2);
  hEnergyLoss2->DrawNormalized("same");


  hEnergyLoss3->SetLineWidth(2);
  hEnergyLoss3->DrawNormalized("same");


  hEnergyLoss4->SetLineColor(kRed);
  hEnergyLoss4->SetLineWidth(2);
  hEnergyLoss4->DrawNormalized("same");


  //hEnergyLoss->Draw();
  //


}
