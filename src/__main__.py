
import web.sigmaweb
print "go"
Sigma = web.sigmaweb.SigmaWebPage()
Sigma.Login("210120810", "154667")

print Sigma.Foto().Data()
print "fim"