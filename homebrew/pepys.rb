class Pepys < Formula
  desc "A Straightforward Markdown Journal"
  homepage "https://lukebriggs.dev/pepys"
  url "https://github.com/LukeBriggsDev/Pepys/archive/refs/tags/v1.3.1.tar.gz"
  sha256 "ed4f71085657dc41f7d044be7961abacd74bf0e678f7ece775b568f326b98ca8"
  license "GPL-3.0"
  depends_on "python@3.8"
  depends_on "pandoc"
  depends_on "enchant"

  def install
    system "#{prefix}/../../../bin/brew", "install", "--cask", "wkhtmltopdf"
    system Formula['python@3.8'].opt_bin/"python3", "-m", "venv", "--system-site-packages", libexec
    system "#{libexec}/bin/pip3.8", "install", "-r", "requirements.txt"
    system "cp", "-R", "src", lib
    system "mkdir", bin
    system "mkdir", "-p","#{bin}/Applications/Pepys.app"
    system "cp", "-R", "homebrew/Pepys.app", "#{bin}/Applications/"
    system "cp", "homebrew/pepys.sh", "#{bin}"
    system "chmod", "+x", "#{bin}/pepys.sh"
  end

  def post_install
    system "open", "#{bin}/Applications"
  end
end
