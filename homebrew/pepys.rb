class Pepys < Formula
  desc "A Straightforward Markdown Journal"
  homepage "https://lukebriggs.dev/pepys"
  url "https://github.com/LukeBriggsDev/Pepys/archive/refs/tags/v1.4.0.tar.gz"
  sha256 "ef8a05efcb77580708f0f13dbb9d5e5b67b8ff20a868a455ad1a68809b0e94c4"
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
  end

  def post_install
    system "open", "#{bin}/Applications"
  end
end
