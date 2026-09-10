import sqlite3
from datetime import datetime
from fpdf import FPDF
 
def safe_text(text):
    if text is None:
        return ""
    replacements = {
        "\u2014": "-",   # em dash
        "\u2013": "-",   # en dash
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2026": "...", # ellipsis
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text.encode("latin-1", "replace").decode("latin-1")
 
DB_FILE = "attack_log.db"
 
class ReportPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, safe_text("LLM Red Teaming Report - SupportBot"), align="L")
        self.cell(0, 10, f"Page {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
 
    def footer(self):
        pass
 
 
def wrap_text(pdf, text, max_width):
    # Simple safeguard against extremely long unbroken strings breaking layout
    return text
 
 
def generate_pdf():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    rows = c.execute("SELECT timestamp, attack_category, prompt, response, succeeded, notes FROM attacks ORDER BY id").fetchall()
    conn.close()
 
    total = len(rows)
    succeeded_count = sum(1 for r in rows if r[4].lower() == "yes")
    success_rate = round(succeeded_count / total * 100, 1) if total else 0
 
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
 
    # Title page
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(20, 20, 20)
    pdf.ln(40)
    pdf.cell(0, 15, "LLM Red Teaming Report", align="C", new_x="LMARGIN", new_y="NEXT")
 
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 10, "SupportBot - Zenith Cloud Storage (Simulated)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
 
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
 
    # Summary stats box
    box_x, box_w = 30, 150
    pdf.set_fill_color(240, 240, 245)
    pdf.rect(box_x, pdf.get_y(), box_w, 45, style="F")
    pdf.set_xy(box_x, pdf.get_y() + 8)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(box_w, 8, "Summary", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(box_x)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(box_w, 8, f"Total attack attempts logged: {total}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(box_x)
    pdf.cell(box_w, 8, f"Successful attacks: {succeeded_count}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(box_x)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(180, 30, 30) if success_rate > 0 else pdf.set_text_color(30, 130, 60)
    pdf.cell(box_w, 8, f"Success rate: {success_rate}%", align="C", new_x="LMARGIN", new_y="NEXT")
 
    # Detailed log
    pdf.add_page()
    pdf.set_text_color(20, 20, 20)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 12, "Detailed Attack Log", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
 
    for i, (ts, category, prompt, response, succeeded, notes) in enumerate(rows, 1):
        succeeded_yes = succeeded.lower() == "yes"
 
        # Entry header bar
        pdf.set_font("Helvetica", "B", 11)
        if succeeded_yes:
            pdf.set_fill_color(250, 225, 225)
            pdf.set_text_color(150, 20, 20)
            status_label = "SUCCEEDED"
        else:
            pdf.set_fill_color(225, 245, 230)
            pdf.set_text_color(20, 110, 50)
            status_label = "FAILED"
 
        pdf.cell(0, 9, safe_text(f"  {i}. {category} - {status_label}"), fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
 
        pdf.set_text_color(90, 90, 90)
        pdf.set_font("Helvetica", "I", 9)
        pdf.cell(0, 6, safe_text(f"Timestamp: {ts}"), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
 
        pdf.set_text_color(20, 20, 20)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, "Prompt:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, safe_text(prompt))
        pdf.ln(1)
 
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, "Response:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, safe_text(response))
 
        if notes:
            pdf.ln(1)
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 6, "Notes:", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 6, safe_text(notes))
 
        pdf.ln(6)
 
    filename = f"redteam_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(filename)
    print(f"PDF report saved to {filename}")
    print(f"{succeeded_count}/{total} attacks succeeded ({success_rate}%)")
 
 
if __name__ == "__main__":
    generate_pdf()