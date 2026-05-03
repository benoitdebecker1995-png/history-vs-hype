"""Generate a professional English translation PDF of the Statut des Juifs.

Design: Clean legal-document typography with generous whitespace,
decorative rules, and consistent article formatting.
"""

from fpdf import FPDF
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent

# ── Fonts ──────────────────────────────────────────────────────
FONT_DIR = Path('C:/Windows/Fonts')
FONTS = {
    '':   FONT_DIR / 'times.ttf',
    'B':  FONT_DIR / 'timesbd.ttf',
    'I':  FONT_DIR / 'timesi.ttf',
    'BI': FONT_DIR / 'timesbi.ttf',
}
FONT_FAMILY = 'TNR'

# ── Color palette ──────────────────────────────────────────────
C_HEADING   = (26, 42, 74)      # dark navy
C_BODY      = (30, 30, 30)      # near-black
C_ACCENT    = (139, 90, 43)     # warm brown
C_NOTE_TEXT = (90, 90, 90)      # medium gray
C_NOTE_BG   = (245, 243, 238)   # warm off-white
C_RULE      = (175, 165, 150)   # warm gray
C_FOOTER    = (130, 130, 130)   # light gray

# ── Spacing constants (mm) ─────────────────────────────────────
MARGIN_LR     = 30
MARGIN_TOP    = 28
MARGIN_BOTTOM = 30
BODY_SIZE     = 11.5
BODY_LEAD     = 6.2
HEADING_SIZE  = 16
NOTE_SIZE     = 10
FOOTER_SIZE   = 8.5


class TranslationPDF(FPDF):
    """Professional legal translation PDF."""

    def setup_fonts(self):
        for style, path in FONTS.items():
            self.add_font(FONT_FAMILY, style, str(path))

    # ── Reusable primitives ────────────────────────────────────

    def _font(self, style='', size=BODY_SIZE):
        self.set_font(FONT_FAMILY, style, size)

    def _color(self, rgb):
        self.set_text_color(*rgb)

    def _draw_color(self, rgb):
        self.set_draw_color(*rgb)

    def thin_rule(self, width=None, center=True):
        """Draw a thin decorative horizontal rule."""
        self._draw_color(C_RULE)
        self.set_line_width(0.3)
        if width and center:
            x_start = (self.w - width) / 2
            self.line(x_start, self.get_y(), x_start + width, self.get_y())
        else:
            self.line(self.l_margin, self.get_y(),
                      self.w - self.r_margin, self.get_y())
        self.set_draw_color(0, 0, 0)

    def ornament(self):
        """Draw a centered ornamental divider (three small squares)."""
        y = self.get_y()
        cx = self.w / 2
        size = 1.2
        gap = 5
        self._draw_color(C_RULE)
        self.set_fill_color(*C_RULE)
        for offset in [-gap, 0, gap]:
            self.rect(cx + offset - size / 2, y - size / 2, size, size, 'F')
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(0, 0, 0)

    # ── Header / Footer ───────────────────────────────────────

    def header(self):
        if self.page_no() <= 2:
            return
        self._font('I', 8)
        self._color(C_FOOTER)
        self.cell(0, 5,
                  'English Translation  \u2014  Statut des Juifs  \u2014  October 3, 1940',
                  align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(1)
        self._draw_color(C_RULE)
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y(),
                  self.w - self.r_margin, self.get_y())
        self.ln(6)
        self.set_draw_color(0, 0, 0)

    def footer(self):
        self.set_y(-MARGIN_BOTTOM + 5)
        if self.page_no() <= 1:
            return
        self._draw_color(C_RULE)
        self.set_line_width(0.15)
        self.line(self.l_margin, self.get_y(),
                  self.w - self.r_margin, self.get_y())
        self.ln(3)
        self._font('', FOOTER_SIZE)
        self._color(C_FOOTER)
        self.cell(0, 5, f'\u2014  {self.page_no()}  \u2014', align='C')

    # ── Title page ─────────────────────────────────────────────

    def title_page(self):
        self.add_page()
        self.ln(45)

        # Decorative rule
        self.thin_rule(width=60)
        self.ln(12)

        # Title
        self._font('', 28)
        self._color(C_HEADING)
        self.multi_cell(0, 12,
                        'Law of October 3, 1940\n'
                        'Concerning the Status of Jews',
                        align='C')
        self.ln(4)

        # French title
        self._font('I', 13)
        self._color(C_ACCENT)
        self.cell(0, 7,
                  'Loi du 3 octobre 1940 portant statut des Juifs',
                  align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(10)

        # Decorative rule
        self.thin_rule(width=60)
        self.ln(14)

        # Subtitle
        self._font('', 13)
        self._color(C_BODY)
        self.cell(0, 7, 'English Translation', align='C',
                  new_x='LMARGIN', new_y='NEXT')
        self.ln(35)

        # Source info block
        self._font('', 10.5)
        self._color(C_NOTE_TEXT)
        lines = [
            'Source: Journal Officiel de la R\u00e9publique Fran\u00e7aise',
            'No. 266, Friday, October 18, 1940',
            'Published at Vichy (Allier)',
        ]
        for line in lines:
            self.cell(0, 6, line, align='C', new_x='LMARGIN', new_y='NEXT')

        self.ln(10)
        self._font('I', 10)
        self.cell(0, 6, 'Translated for History vs Hype',
                  align='C', new_x='LMARGIN', new_y='NEXT')

    # ── Translator's note page ─────────────────────────────────

    def translators_note(self):
        self.add_page()
        self.ln(5)

        self._font('', 16)
        self._color(C_HEADING)
        self.cell(0, 10, "Translator\u2019s Note", align='C',
                  new_x='LMARGIN', new_y='NEXT')
        self.ln(3)
        self.thin_rule(width=40)
        self.ln(10)

        self._font('', BODY_SIZE)
        self._color(C_BODY)

        paras = [
            'This is an English translation of the Loi du 3 octobre 1940 '
            'portant statut des Juifs (Law of October 3, 1940, Concerning the '
            'Status of Jews), the first major piece of anti-Jewish legislation '
            'enacted by the Vichy regime. The law was drafted by Rapha\u00ebl '
            'Alibert, Minister of Justice, and signed by Marshal P\u00e9tain and '
            'nine ministers of the Vichy cabinet.',

            'The French text is taken from the Journal Officiel de la '
            'R\u00e9publique Fran\u00e7aise, No. 266, published on October 18, '
            '1940. The law was enacted on October 3 but not published until '
            'fifteen days later.',

            'This translation follows the legal structure of the original: '
            'ten articles progressing from the racial definition of '
            '\u201cJewish\u201d (Article 1), through comprehensive professional '
            'exclusions (Articles 2\u20136), to implementation mechanisms '
            '(Articles 7\u201310). Where French legal terminology has no exact '
            'English equivalent, the closest functional translation is used '
            'with the original French term noted.',

            'Three features of the text deserve attention:',
        ]
        for para in paras:
            self.multi_cell(0, BODY_LEAD, para, align='J')
            self.ln(3)

        # Numbered observations
        points = [
            ('The law uses \u201crace juive\u201d (Jewish race) throughout, '
             'never \u201creligion juive\u201d (Jewish religion). This is a '
             'racial statute, not a religious restriction.'),
            ('Article 4 uses the word \u201c\u00e9limination\u201d to describe '
             'removing Jews from professions. While this was standard '
             'bureaucratic French in 1940, the word is preserved in '
             'translation as \u201celimination\u201d to reflect the original language.'),
            ('No provision of this law references Germany, the armistice, '
             'or the occupation. It reads as a purely French initiative, '
             'because it was.'),
        ]
        for i, text in enumerate(points, 1):
            x = self.get_x()
            self._font('', BODY_SIZE)
            self.cell(8, BODY_LEAD, f'{i}.', align='R')
            self.set_x(x + 10)
            self.multi_cell(self.w - self.l_margin - self.r_margin - 10,
                            BODY_LEAD, text, align='J')
            self.ln(2)

    # ── Content helpers ────────────────────────────────────────

    def article_heading(self, text):
        """Centered article heading with decorative rules above and below.
        Ensures at least 50mm of space below so it won't be orphaned."""
        space_left = self.h - self.b_margin - self.get_y()
        if space_left < 50:
            self.add_page()
        self.ln(8)
        self.thin_rule(width=30)
        self.ln(5)
        self._font('', HEADING_SIZE)
        self._color(C_HEADING)
        self.cell(0, 9, text, align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(3)
        self.thin_rule(width=30)
        self.ln(7)

    def body(self, text):
        """Standard justified body text."""
        self._font('', BODY_SIZE)
        self._color(C_BODY)
        self.multi_cell(0, BODY_LEAD, text, align='J')
        self.ln(3)

    def body_indent(self, text, indent=8):
        """Indented body text for sub-items."""
        self._font('', BODY_SIZE)
        self._color(C_BODY)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent,
                        BODY_LEAD, text, align='J')
        self.ln(2)

    def numbered_item(self, number, text):
        """Numbered list item with hanging indent."""
        self._font('', BODY_SIZE)
        self._color(C_BODY)
        x = self.get_x()
        indent = 10
        self.cell(indent, BODY_LEAD, f'{number}.', align='R')
        self.set_x(x + indent + 2)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent - 2,
                        BODY_LEAD, text, align='J')
        self.ln(2)

    def lettered_item(self, letter, text):
        """Lettered list item with hanging indent."""
        self._font('', BODY_SIZE)
        self._color(C_BODY)
        x = self.get_x()
        indent = 14
        self.cell(indent, BODY_LEAD, f'{letter}.', align='R')
        self.set_x(x + indent + 2)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent - 2,
                        BODY_LEAD, text, align='J')
        self.ln(2)

    def preamble_line(self, text):
        """Preamble text (slightly larger, centered feel)."""
        self._font('', 12)
        self._color(C_BODY)
        self.multi_cell(0, 7, text, align='L')
        self.ln(1.5)

    def signatory_name(self, text):
        """Signatory entry."""
        self._font('', 11)
        self._color(C_BODY)
        self.multi_cell(0, 6.5, text, align='L')
        self.ln(2)

    def signatory_head(self, text):
        """Head of State signatory (larger, italic)."""
        self._font('I', 13)
        self._color(C_BODY)
        self.multi_cell(0, 7, text, align='L')
        self.ln(3)


def build_pdf():
    pdf = TranslationPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=MARGIN_BOTTOM)
    pdf.set_margins(MARGIN_LR, MARGIN_TOP, MARGIN_LR)
    pdf.setup_fonts()

    # ═══════════════════════════════════════════════════════════
    # TITLE PAGE
    # ═══════════════════════════════════════════════════════════
    pdf.title_page()

    # ═══════════════════════════════════════════════════════════
    # TRANSLATOR'S NOTE
    # ═══════════════════════════════════════════════════════════
    pdf.translators_note()

    # ═══════════════════════════════════════════════════════════
    # LAW TEXT — PREAMBLE + ARTICLE 1
    # ═══════════════════════════════════════════════════════════
    pdf.add_page()

    # Law title
    pdf.ln(2)
    pdf._font('', 18)
    pdf._color(C_HEADING)
    pdf.cell(0, 10, 'LAW CONCERNING THE STATUS OF JEWS',
             align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(8)

    # Preamble
    pdf.preamble_line(
        'We, Marshal of France, Head of the French State,')
    pdf.preamble_line(
        'The Council of Ministers having been heard,')
    pdf.preamble_line('Decree:')
    pdf.ln(2)

    # Article 1
    pdf.article_heading('Article 1')
    pdf.body(
        'For the application of the present law, any person descended from '
        'three grandparents of the Jewish race, or from two grandparents of '
        'the same race if their spouse is themselves Jewish, is regarded as '
        'Jewish.'
    )

    # ═══════════════════════════════════════════════════════════
    # ARTICLE 2
    # ═══════════════════════════════════════════════════════════
    pdf.article_heading('Article 2')
    pdf.body(
        'Access to and exercise of the public functions and offices listed '
        'below are forbidden to Jews:'
    )

    pdf.numbered_item(1,
        'Head of State, member of the Government, Council of State, '
        'Council of the National Order of the Legion of Honor, Court of '
        'Cassation, Court of Auditors, Corps of Mines, Corps of Bridges '
        'and Roads, General Inspectorate of Finance, Courts of Appeal, '
        'Courts of First Instance, Justices of the Peace, all professional '
        'courts and all elected assemblies;')

    pdf.numbered_item(2,
        'Officials of the Department of Foreign Affairs, '
        'secretaries-general of ministerial departments, '
        'directors-general, directors of central ministry '
        'administrations, prefects, sub-prefects, secretaries-general '
        'of prefectures, inspectors-general of administrative services '
        'at the Ministry of the Interior, civil servants of all grades '
        'attached to all police services;')

    pdf.numbered_item(3,
        'Residents-general, governors-general, governors and '
        'secretaries-general of the colonies, inspectors of the colonies;')

    pdf.numbered_item(4, 'Members of teaching bodies;')

    pdf.numbered_item(5,
        'Officers of the Army, Navy, and Air Force;')

    pdf.numbered_item(6,
        'Administrators, directors, secretaries-general in enterprises '
        'receiving concessions or subsidies from a public authority, '
        'positions appointed by the Government in enterprises of general '
        'interest.')

    # ═══════════════════════════════════════════════════════════
    # ARTICLE 3
    # ═══════════════════════════════════════════════════════════
    pdf.article_heading('Article 3')
    pdf.body(
        'Access to and exercise of all public functions other than those '
        'listed in Article 2 are open to Jews only if they can invoke one '
        'of the following conditions:'
    )

    pdf.numbered_item(1,
        'To hold the Veteran\u2019s Card of 1914\u20131918 or to have been '
        'mentioned in dispatches during the 1914\u20131918 campaign;')

    pdf.numbered_item(2,
        'To have been mentioned in dispatches during the 1939\u20131940 '
        'campaign;')

    pdf.numbered_item(3,
        'To be decorated with the Legion of Honor for military service '
        'or with the Military Medal.')

    # ═══════════════════════════════════════════════════════════
    # ARTICLE 4
    # ═══════════════════════════════════════════════════════════
    pdf.article_heading('Article 4')
    pdf.body(
        'Access to and exercise of the liberal professions, independent '
        'professions, functions assigned to ministerial officers and to '
        'all auxiliaries of justice are permitted to Jews, unless public '
        'administrative regulations have fixed a determined proportion '
        'for them. In that case, the same regulations shall determine the '
        'conditions under which the elimination of excess Jews shall '
        'take place.'
    )

    # ═══════════════════════════════════════════════════════════
    # ARTICLE 5
    # ═══════════════════════════════════════════════════════════
    pdf.article_heading('Article 5')
    pdf.body(
        'Jews may not, without condition or reservation, exercise any of '
        'the following professions:'
    )
    pdf.body_indent(
        'Directors, managers, editors of newspapers, magazines, agencies, '
        'or periodicals, with the exception of publications of a strictly '
        'scientific character.'
    )
    pdf.body_indent(
        'Directors, administrators, managers of enterprises engaged in the '
        'manufacture, printing, distribution, or presentation of '
        'cinematographic films; film directors and directors of photography, '
        'screenwriters, directors, administrators, managers of theaters or '
        'cinemas, entertainment producers, directors, administrators, '
        'managers of all enterprises related to radio broadcasting.'
    )
    pdf.body(
        'Public administrative regulations shall determine, for each '
        'category, the conditions under which public authorities may ensure '
        'compliance by the relevant parties with the prohibitions pronounced '
        'in the present article, as well as the sanctions attached to these '
        'prohibitions.'
    )

    # ═══════════════════════════════════════════════════════════
    # ARTICLE 6
    # ═══════════════════════════════════════════════════════════
    pdf.article_heading('Article 6')
    pdf.body(
        'Under no circumstances may Jews be members of organizations '
        'charged with representing the professions referred to in '
        'Articles 4 and 5 of the present law or with ensuring their '
        'discipline.'
    )

    # ═══════════════════════════════════════════════════════════
    # ARTICLE 7
    # ═══════════════════════════════════════════════════════════
    pdf.article_heading('Article 7')
    pdf.body(
        'Jewish civil servants covered by Articles 2 and 3 shall cease '
        'exercising their functions within two months following the '
        'promulgation of the present law. They shall be entitled to claim '
        'their pension rights, if they meet the conditions of length of '
        'service; to a proportional pension, if they have at least fifteen '
        'years of service; those unable to invoke either of these conditions '
        'shall receive their salary for a period to be determined, for each '
        'category, by a public administrative regulation.'
    )

    # ═══════════════════════════════════════════════════════════
    # ARTICLE 8
    # ═══════════════════════════════════════════════════════════
    pdf.article_heading('Article 8')
    pdf.body(
        'By individual decree issued by the Council of State and duly '
        'justified, Jews who, in the literary, scientific, or artistic '
        'domains, have rendered exceptional services to the French State, '
        'may be relieved of the prohibitions provided for by the present '
        'law.'
    )
    pdf.body(
        'These decrees and the grounds justifying them shall be published '
        'in the Journal Officiel.'
    )

    # ═══════════════════════════════════════════════════════════
    # ARTICLE 9
    # ═══════════════════════════════════════════════════════════
    pdf.article_heading('Article 9')
    pdf.body(
        'The present law is applicable to Algeria, to the colonies, '
        'protectorate countries, and mandated territories.'
    )

    # ═══════════════════════════════════════════════════════════
    # ARTICLE 10
    # ═══════════════════════════════════════════════════════════
    pdf.article_heading('Article 10')
    pdf.body(
        'The present act shall be published in the Journal Officiel and '
        'executed as a law of the State.'
    )

    # ═══════════════════════════════════════════════════════════
    # SIGNATORIES
    # ═══════════════════════════════════════════════════════════
    pdf.ln(4)
    pdf.ornament()
    pdf.ln(10)

    pdf._font('', 12)
    pdf._color(C_BODY)
    pdf.cell(0, 7, 'Done at Vichy, October 3, 1940.',
             new_x='LMARGIN', new_y='NEXT')
    pdf.ln(6)

    pdf.signatory_head('Ph. P\u00e9tain.')
    pdf.ln(4)

    pdf._font('', 11)
    pdf._color(C_BODY)
    pdf.cell(0, 6.5,
             'By the Marshal of France, Head of the French State:',
             new_x='LMARGIN', new_y='NEXT')
    pdf.ln(4)

    signatories = [
        'The Vice-President of the Council, Pierre Laval.',
        'The Keeper of the Seals, Minister Secretary of State '
        'for Justice, Rapha\u00ebl Alibert.',
        'The Minister Secretary of State for the Interior, '
        'Marcel Peyrouton.',
        'The Minister Secretary of State for Foreign Affairs, '
        'Paul Baudoin.',
        'The Minister Secretary of State for War, '
        'General Huntziger.',
        'The Minister Secretary of State for Finance, '
        'Yves Bouthillier.',
        'The Minister Secretary of State for the Navy, '
        'Admiral Darlan.',
        'The Minister Secretary of State for Industrial Production '
        'and Labor, Ren\u00e9 Belin.',
        'The Minister Secretary of State for Agriculture, '
        'Pierre Caziot.',
    ]
    for sig in signatories:
        pdf.signatory_name(sig)

    # ═══════════════════════════════════════════════════════════
    # SOURCE REFERENCE (final page)
    # ═══════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.ln(20)

    pdf._font('', 14)
    pdf._color(C_HEADING)
    pdf.cell(0, 8, 'Source', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)
    pdf.thin_rule(width=30)
    pdf.ln(10)

    pdf._font('', NOTE_SIZE + 1)
    pdf._color(C_BODY)
    source_lines = [
        'Journal Officiel de la R\u00e9publique Fran\u00e7aise',
        'No. 266, Friday, October 18, 1940',
        'Pages 5323\u20135324',
        'Published at Vichy (Allier)',
    ]
    for line in source_lines:
        pdf.cell(0, 6.5, line, align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.ln(15)
    pdf._font('I', NOTE_SIZE)
    pdf._color(C_NOTE_TEXT)
    pdf.multi_cell(0, 5.5,
        'The Statut des Juifs was enacted on October 3, 1940, and '
        'published in the Journal Officiel fifteen days later on '
        'October 18. It was the first major piece of anti-Jewish '
        'legislation passed by the Vichy government. The law was drafted '
        'without German pressure or instruction; it was an autonomous '
        'act of the French State.',
        align='C')

    pdf.ln(20)
    pdf.ornament()
    pdf.ln(10)
    pdf._font('I', 9)
    pdf._color(C_FOOTER)
    pdf.cell(0, 5, 'History vs Hype', align='C')

    # ── Save ───────────────────────────────────────────────────
    out = OUTPUT_DIR / 'LAW OF OCTOBER 3, 1940, CONCERNING THE STATUS OF JEWS.pdf'
    pdf.output(str(out))
    print(f'PDF saved to: {out}')
    return out


if __name__ == '__main__':
    build_pdf()
