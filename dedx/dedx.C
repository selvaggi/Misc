#include "TH1F.h"
#include "TMath.h"
#include "TLorentzVector.h"


Int_t NEVENTS=100000;


// formula Taken from Leo (2.30) pg. 26
double deltaf(double c0, double a, double m, double x0, double x1, double beta, double gamma)
{
   Double_t x= TMath::Log10(beta*gamma);
   delta = 0.;
   
   //cout<<x<<","<<x0<<","<<x1<<","<<endl;
   
   if (x < x0)
       delta = 0.;
   if (x >= x0 && x< x1)
       delta = 4.6052*x - c0 + a*TMath::Power(x1 - x,m);
   if  (x> x1)
       delta = 4.6052*x - c0;
       
   return delta;
}

//------------------------------------------------------------------------------

void dedx()
{
  TH1F *hEnergyLoss = new TH1F("energy_loss", "energy_loss", 100, 0.4, 1.0);

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
   
  // print particle properties
  cout<<"E: "<<pvec.E()<<", P: "<<pvec.P()<<", Pt: "<<pvec.Pt()<<", M: "<<pvec.M()<<", Beta: "<< pvec.Beta()<<", Gamma: "<<pvec.Gamma() <<", Charge: "<<charge<<endl;   
  

  /*

Index =   14:  silicon (Si)
     Absorber with Z =  14,  A = 28.0855(3), density = 2.329 (revised)
 Sternheimer coef:  a     k=m_s   x_0    x_1    I[eV]   Cbar  delta0 
                 0.1492  3.2546  0.2015  2.8716  173.0  4.4355 0.14

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
  Double_t c0      = 4.4355;
     
  */
  
  /*


     Absorber with Z =  18,  A = 39.948(1), density = $ 1.662 \times10^{- 3}$          
 Sternheimer coef:  a     k=m_s   x_0    x_1    I[eV]   Cbar  delta0 
                 0.1971  2.9618  1.7635  4.4855  188.0 11.9480 0.00

*/

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
  

   
  // how much matter are we traversing in cm
  Double_t x = 100; // 1.7 mm in Silicon  
  //Double_t x = 1.; // 1.7 mm in Silicon
   
  // formula (33.12) from http://pdg.lbl.gov/2019/reviews/rpp2018-rev-passage-particles-matter.pdf
  Double_t kappa = 2*0.1535*TMath::Abs(charge)*TMath::Abs(charge)*Z*rho*x/(A*beta*beta); //energy loss in MeV
  Double_t chi = 0.5*kappa;
  Double_t me = 0.510998; // electron mass in MeV, need  
  I *= 1e-6; // convert I in MeV
  Double_t Wmax = 2*me*beta*beta*gamma*gamma; // this is not valid for electrons
  Double_t delta = deltaf(c0, a, m, x0, x1, beta, gamma);
 
  //Double_t DeDx= chi*( 2*TMath::Log(Wmax/I) - 2*beta*beta - delta);  
  Double_t DeDx = kappa*( TMath::Log(Wmax/I) - beta*beta - delta/2);  
  Double_t DeltaP = chi*( TMath::Log(Wmax/I) + TMath::Log(chi/I) + 0.2 - beta*beta - delta);  
  
  cout<<"Wmax: "<<Wmax<<", Chi: "<<chi<<", delta: "<<delta<<", DeDx: "<<DeDx<<", DeltaP: "<<DeltaP<<endl;

  // event loop
  
  for (int i=0; i<NEVENTS; i++)
  {
     
     Double_t eloss = gRandom->Landau(DeltaP,chi); // this is the total energy loss in MeV
     //Double_t eloss = gRandom->Uniform();
    
     hEnergyLoss->Fill(eloss);
     //cout<<eloss<<endl;
     
  }
  
  hEnergyLoss->Draw();
}
