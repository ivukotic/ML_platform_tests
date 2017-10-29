from ROOT import *
import numpy as np

doeasy = False #if easy, then we get two Gaussians, otherwise, many Gaussians!

def mycopy(myinput):
  myoutput = TH1F("","",myinput.GetNbinsX(),myinput.GetXaxis().GetBinCenter(1)-0.5*myinput.GetXaxis().GetBinWidth(1),myinput.GetXaxis().GetBinCenter(myinput.GetNbinsX())+0.5*myinput.GetXaxis().GetBinWidth(myinput.GetNbinsX()))
  for i in range(1,myinput.GetNbinsX()+1):
    myoutput.SetBinContent(i,myinput.GetBinContent(i))
    myoutput.SetBinError(i,0.)
    pass
  return myoutput

mygraphS = TH1F("","",500,-5,5)
mygraphB = TH1F("","",500,-5,5)
mygraphLL = TH1F("","",500,-5,5)

for i in range(1,mygraphS.GetNbinsX()+1):
	myxval = mygraphS.GetXaxis().GetBinCenter(i)
	if (doeasy):
		mygraphS.SetBinContent(i,ROOT.Math.gaussian_pdf(myxval,1,1))
		mygraphB.SetBinContent(i,ROOT.Math.gaussian_pdf(myxval,1,-1))
		pass
	if (doeasy==False):
		mygraphS.SetBinContent(i,ROOT.Math.gaussian_pdf(myxval,0.5,2.)+0.5*ROOT.Math.gaussian_pdf(myxval,1,-1))
		mygraphB.SetBinContent(i,0.8*ROOT.Math.gaussian_pdf(myxval,0.5,-1.1)+0.5*ROOT.Math.gaussian_pdf(myxval,1,1))
		pass
	pass

for i in range(1,mygraphS.GetNbinsX()+1):
	if (mygraphB.GetBinContent(i) > 0 and mygraphS.GetBinContent(i) > 0):
		mygraphLL.SetBinContent(i,mygraphS.GetBinContent(i)/mygraphB.GetBinContent(i))
	elif (mygraphS.GetBinContent(i) > 0):
		mygraphLL.SetBinContent(i,100000.)
	elif (mygraphB.GetBinContent(i) > 0):
		mygraphLL.SetBinContent(i,1./100000.)
	else: 
		mygraphLL.SetBinContent(i,1)
	pass

yvalsS={}
yvalsB={}

xvals_log = []

for i in range(1,mygraphS.GetNbinsX()+1):
	yvalsS[mygraphLL.GetBinContent(i)]=0.
	yvalsB[mygraphLL.GetBinContent(i)]=0.
	xvals_log+=[mygraphLL.GetBinContent(i)]
	pass

xvals_log = np.sort(xvals_log)

yvalsS_h = TH1F("","",len(xvals_log)-1,np.array(xvals_log))
yvalsB_h = TH1F("","",len(xvals_log)-1,np.array(xvals_log))

myss = 0.
for i in range(1,mygraphS.GetNbinsX()+1):
	yvalsS[mygraphLL.GetBinContent(i)]=yvalsS[mygraphLL.GetBinContent(i)]+mygraphS.GetBinContent(i)
	yvalsB[mygraphLL.GetBinContent(i)]=yvalsB[mygraphLL.GetBinContent(i)]+mygraphB.GetBinContent(i)
	myss+=mygraphS.GetBinContent(i)
	#print i,mygraphLL.GetBinContent(i),yvalsS[mygraphLL.GetBinContent(i)],yvalsB[mygraphLL.GetBinContent(i)]
	yvalsS_h.Fill(mygraphLL.GetBinContent(i),mygraphS.GetBinContent(i))
	yvalsB_h.Fill(mygraphLL.GetBinContent(i),mygraphB.GetBinContent(i))
	pass

yvalsS_h.Scale(1./yvalsS_h.Integral())
yvalsB_h.Scale(1./yvalsB_h.Integral())

for i in range(1,yvalsS_h.GetNbinsX()+1):
	yvalsS_h.SetBinError(i,0.)
	yvalsB_h.SetBinError(i,0.)

print myss

c = TCanvas("a","a",500,500)

gPad.SetLeftMargin(0.15)
gPad.SetBottomMargin(0.15)
gPad.SetTopMargin(0.05)
gPad.SetRightMargin(0.05)

mygraphS.Scale(1./mygraphS.Integral())
mygraphB.Scale(1./mygraphB.Integral())
mygraphS = mycopy(mygraphS)
mygraphB = mycopy(mygraphB)

mygraphS.SetLineColor(1)
mygraphS.SetLineWidth(2)
mygraphS.GetXaxis().SetTitleOffset(1.8)
mygraphS.GetYaxis().SetTitleOffset(1.8)

gStyle.SetOptStat(0)
mygraphS.SetLineWidth(2)
mygraphS.SetLineColor(2)
mygraphB.SetLineWidth(2)
mygraphB.SetLineColor(4)

mygraphS.GetXaxis().SetTitle("Input feature x")
mygraphS.GetYaxis().SetTitle("Probability Distribution Function")
mygraphS.GetXaxis().SetTitleOffset(1.8)
mygraphS.GetYaxis().SetTitleOffset(2.2)
mygraphS.GetYaxis().SetNdivisions(505)

leg = TLegend(.19,.8,.39,.92)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(mygraphS,"Signal","l")
leg.AddEntry(mygraphB,"Background","l")

mygraphS.Draw("")
mygraphB.Draw("same")

leg.Draw()

c.Print("test.pdf")

gPad.SetLogx()
gPad.SetLogy()

yvalsS_h.GetXaxis().SetTitle("Likelihood Ratio")
yvalsS_h.GetYaxis().SetTitle("Probability Distribution Function")
yvalsS_h.GetXaxis().SetTitleOffset(1.8)
yvalsS_h.GetYaxis().SetTitleOffset(2.2)

yvalsS_h.SetLineColor(2)
yvalsB_h.SetLineColor(4)
yvalsS_h.GetYaxis().SetRangeUser(min(yvalsS_h.GetBinContent(1),yvalsB_h.GetBinContent(1)),yvalsS_h.GetMaximum()*100)
yvalsS_h.Draw()
yvalsB_h.Draw("same")

leg = TLegend(.19,.8,.39,.92)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(yvalsS_h,"Signal","l")
leg.AddEntry(yvalsB_h,"Background","l")

leg.Draw()

c.Print("LLdist.pdf")
gPad.SetLogx(0)
gPad.SetLogy(0)

xx = []
ys = []
yb = []

myss = 0.
for mytag in yvalsS:
	xx+=[mytag]
	pass

xx = np.sort(xx)
for x in xx:
	ys+=[yvalsS[x]]
	yb+=[yvalsB[x]]
	myss+=yvalsS[x]
	print x,yvalsS[x],yvalsB[x]
	pass

print myss

mygraphS = TGraph(len(xx),np.array(xx),np.array(ys))
mygraphB = TGraph(len(xx),np.array(xx),np.array(yb))

gPad.SetLogx()
mygraphS.SetLineWidth(2)
mygraphS.SetLineColor(2)
mygraphB.SetLineWidth(2)
mygraphB.SetLineColor(4)

mygraphS.SetMarkerColor(2)
mygraphB.SetMarkerColor(4)
mygraphS.SetMarkerSize(1)
mygraphS.SetMarkerStyle(20)
mygraphB.SetMarkerSize(1)
mygraphB.SetMarkerStyle(21)

mygraphS.SetTitle("")
mygraphS.Draw("ap")
mygraphB.Draw("samep")
#c.Print("test2.pdf")

gPad.SetLogx(0)
gPad.SetLogy(1)
gPad.SetLeftMargin(0.15)
gPad.SetBottomMargin(0.15)
gPad.SetTopMargin(0.05)
gPad.SetRightMargin(0.05)
mygraphLL.SetLineColor(1)
mygraphLL.SetLineWidth(2)
mygraphLL.Draw("c")
mygraphLL.GetXaxis().SetTitleOffset(1.8)
mygraphLL.GetYaxis().SetTitleOffset(2.2)
mygraphLL.GetXaxis().SetTitle("Input feature x")
mygraphLL.GetYaxis().SetTitle("Likelihood Ratio")
c.Print("LL.pdf")

xx=np.sort(xx)
xx = sorted(xx, reverse=True)

ROCx =[]
ROCy =[]

mysum = 0.
mysum2 = 0.

for x in xx:
	ROCx+=[mysum]
	mysum+=yvalsS[x]

	ROCy+=[mysum2]
	mysum2+=yvalsB[x]
	pass

for i in range(len(ROCx)):
	ROCx[i] = ROCx[i] / mysum
	ROCy[i] = ROCy[i] / mysum2
	pass

gPad.SetLogy(0)
gPad.SetLeftMargin(0.15)
gPad.SetBottomMargin(0.15)
gPad.SetTopMargin(0.05)
gPad.SetRightMargin(0.05)
myroc = TGraph(len(ROCx),np.array(ROCx),np.array(ROCy))
myroc.SetTitle("")
myroc.GetXaxis().SetRangeUser(0,1)
myroc.GetYaxis().SetRangeUser(0,1)
myroc.SetLineColor(1)
myroc.GetYaxis().SetNdivisions(505)
myroc.SetMarkerColor(1)
myroc.SetMarkerStyle(20)
myroc.SetMarkerSize(1)
myroc.SetLineWidth(2)
myroc.GetXaxis().SetTitle("Pr(#color[4]{#bf{label signal}} | #bf{#color[4]{signal}})")
myroc.GetYaxis().SetTitle("Pr(#color[4]{#bf{label signal}} | #bf{#color[2]{background}})")
myroc.GetXaxis().SetTitleOffset(1.8)
myroc.GetYaxis().SetTitleOffset(2.2)
myroc.Draw("ca")
myline = TLine(0,0,1,1)
myline.SetLineStyle(3)
myline.Draw()
c.Print("ROC.pdf")

