class Pepys < Formula
  desc "A Straightforward Markdown Journal"
  homepage "https://lukebriggs.dev/pepys"
  url "https://github.com/LukeBriggsDev/Pepys/archive/refs/tags/v1.2.0.tar.gz"
  sha256 "334d89044033ec975687b2a7523b9022a22f816f51a534e5232f2d6158f46955"
  license "GPL-3.0"
  depends_on "python@3.8"
  depends_on "pandoc"
  depends_on "enchant"

  def install
    system "/opt/homebrew/bin/brew", "install", "--cask", "wkhtmltopdf"
    system Formula['python@3.8'].opt_bin/"python3", "-m", "venv", "--system-site-packages", libexec
    system "#{libexec}/bin/pip3.8", "install", "-r", "requirements.txt"
    system "cp", "-R", "src", lib
    system "mkdir", bin
    system "cp", "homebrew/pepys.sh", "#{bin}"
    system "cp", "-R", "homebrew/Pepys.app", "~/Applications"
    system "chmod", "+x", "#{bin}/pepys.sh"
  end
end
