const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const dns = require('dns');

const app = express();
const PORT = 3000;

const DATA_FILE = path.join(__dirname, 'blocked_domains.json');

app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

function loadBlockedDomains() {
  if (!fs.existsSync(DATA_FILE)) return {};
  return JSON.parse(fs.readFileSync(DATA_FILE));
}

function saveBlockedDomains(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

function resolveDomain(domain) {
  return new Promise((resolve, reject) => {
    dns.resolve4(domain, (err, addresses) => {
      if (err) reject(err);
      else resolve(addresses);
    });
  });
}

function blockIP(ip) {
  ['in', 'out'].forEach(dir => {
    try {
      execSync(`netsh advfirewall firewall add rule name=Block_${ip}_${dir} dir=${dir} action=block remoteip=${ip} protocol=ANY`);
    } catch (err) {
      console.error(`Failed to block ${ip}:`, err);
    }
  });
}

function unblockIP(ip) {
  ['in', 'out'].forEach(dir => {
    try {
      execSync(`netsh advfirewall firewall delete rule name=Block_${ip}_${dir}`);
    } catch (err) {
      console.error(`Failed to unblock ${ip}:`, err);
    }
  });
}

app.get('/', (req, res) => {
  const domains = loadBlockedDomains();
  res.render('index', { blocked: domains });
});

app.post('/block', async (req, res) => {
  const domain = req.body.block_domain;
  const domains = loadBlockedDomains();
  try {
    const resolvedIPs = await resolveDomain(domain);
    domains[domain] = resolvedIPs;
    resolvedIPs.forEach(ip => blockIP(ip));
    saveBlockedDomains(domains);
    res.redirect('/');
  } catch (err) {
    console.error('DNS resolve failed:', err);
    res.send('Failed to resolve domain');
  }
});

app.post('/unblock', (req, res) => {
  const domain = req.body.unblock_domain;
  const domains = loadBlockedDomains();
  if (domains[domain]) {
    domains[domain].forEach(ip => unblockIP(ip));
    delete domains[domain];
    saveBlockedDomains(domains);
  }
  res.redirect('/');
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
