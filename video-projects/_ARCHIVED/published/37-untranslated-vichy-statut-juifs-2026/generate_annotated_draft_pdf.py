"""Generate professional annotated draft translation PDF.

Shows Pétain's handwritten changes to the typed Statut des Juifs draft.
Visual conventions:
  - Regular black text  = typed draft
  - Bold blue text      = Pétain's handwritten additions
  - Red strikethrough   = text Pétain struck out
  - Gray italic in []   = translator's note

Source: Five-page typed draft with handwritten annotations,
discovered by Serge Klarsfeld, announced October 3, 2010,
at the Mémorial de la Shoah, Paris.
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
C_HEADING    = (26, 42, 74)       # dark navy
C_BODY       = (30, 30, 30)       # near-black
C_INK        = (25, 25, 112)      # Pétain's ink (dark blue)
C_STRIKE     = (170, 30, 30)      # struck-through text (dark red)
C_NOTE_TEXT  = (100, 100, 100)    # translator's notes
C_NOTE_BG    = (245, 243, 238)    # note background
C_RULE       = (175, 165, 150)    # decorative rules
C_FOOTER     = (130, 130, 130)    # footer text
C_CONF       = (170, 30, 30)      # DOCUMENT CONFIDENTIEL
C_ACCENT     = (139, 90, 43)      # warm brown accent
C_ANNOT_BORDER = (60, 60, 140)    # annotation box left border

# ── Spacing ────────────────────────────────────────────────────
MARGIN_LR     = 28
MARGIN_TOP    = 28
MARGIN_BOTTOM = 28
BODY_SIZE     = 11.5
BODY_LEAD     = 6.2
NOTE_SIZE     = 10
HEADING_SIZE  = 16


class AnnotatedDraftPDF(FPDF):
    """Professional annotated draft PDF with color-coded annotations."""

    def setup_fonts(self):
        for style, path in FONTS.items():
            self.add_font(FONT_FAMILY, style, str(path))

    # ── Primitives ─────────────────────────────────────────────

    def _font(self, style='', size=BODY_SIZE):
        self.set_font(FONT_FAMILY, style, size)

    def _color(self, rgb):
        self.set_text_color(*rgb)

    def _draw_color(self, rgb):
        self.set_draw_color(*rgb)

    def thin_rule(self, width=None, center=True):
        self._draw_color(C_RULE)
        self.set_line_width(0.3)
        if width and center:
            x = (self.w - width) / 2
            self.line(x, self.get_y(), x + width, self.get_y())
        else:
            self.line(self.l_margin, self.get_y(),
                      self.w - self.r_margin, self.get_y())
        self.set_draw_color(0, 0, 0)

    def ornament(self):
        y = self.get_y()
        cx = self.w / 2
        s = 1.2
        gap = 5
        self.set_fill_color(*C_RULE)
        for off in [-gap, 0, gap]:
            self.rect(cx + off - s / 2, y - s / 2, s, s, 'F')
        self.set_fill_color(255, 255, 255)

    def annotation_box_start(self):
        """Draw a left-border accent line for annotation blocks."""
        self._x_annot_start = self.get_y()
        self._x_annot_x = self.l_margin - 2

    def annotation_box_end(self):
        y_end = self.get_y()
        self._draw_color(C_ANNOT_BORDER)
        self.set_line_width(0.8)
        self.line(self._x_annot_x, self._x_annot_start,
                  self._x_annot_x, y_end)
        self.set_line_width(0.3)
        self.set_draw_color(0, 0, 0)

    # ── Header / Footer ───────────────────────────────────────

    def header(self):
        if self.page_no() <= 2:
            return
        self._font('I', 8)
        self._color(C_FOOTER)
        self.cell(0, 5,
                  'Annotated Draft  \u2014  Statut des Juifs  \u2014  October 3, 1940',
                  align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(1)
        self._draw_color(C_RULE)
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y(),
                  self.w - self.r_margin, self.get_y())
        self.ln(5)
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
        self._font('', 8.5)
        self._color(C_FOOTER)
        self.cell(0, 5, f'\u2014  {self.page_no()}  \u2014', align='C')

    # ── Title page ─────────────────────────────────────────────

    def title_page(self):
        self.add_page()
        self.ln(30)

        # DOCUMENT CONFIDENTIEL
        self._font('B', 13)
        self._color(C_CONF)
        self.cell(0, 8, 'DOCUMENT CONFIDENTIEL', align='C',
                  new_x='LMARGIN', new_y='NEXT')
        self.ln(5)

        # Projet
        self._font('I', 12)
        self._color(C_ACCENT)
        self.cell(0, 7, 'Projet', align='C',
                  new_x='LMARGIN', new_y='NEXT')
        self.ln(12)

        # Decorative rule
        self.thin_rule(width=60)
        self.ln(10)

        # Title
        self._font('', 26)
        self._color(C_HEADING)
        self.multi_cell(0, 11,
                        'Annotated Draft\n'
                        'Law of October 3, 1940\n'
                        'Concerning the Status of Jews',
                        align='C')
        self.ln(4)

        # French subtitle
        self._font('I', 12)
        self._color(C_ACCENT)
        self.cell(0, 7,
                  'Loi du 3 octobre 1940 portant statut des Juifs',
                  align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(8)

        # Decorative rule
        self.thin_rule(width=60)
        self.ln(14)

        # Description
        self._font('', 11)
        self._color(C_BODY)
        self.multi_cell(0, 6,
            'Typed draft with handwritten annotations by Marshal P\u00e9tain',
            align='C')
        self.ln(30)

        # Provenance block
        self._font('', 10)
        self._color(C_NOTE_TEXT)
        provenance = [
            'Source: M\u00e9morial de la Shoah, Paris',
            'Five-page typed draft with handwritten annotations',
            'Discovered by Serge Klarsfeld',
            'Announced October 3, 2010, on the 70th anniversary of the statute',
        ]
        for line in provenance:
            self.cell(0, 5.5, line, align='C',
                      new_x='LMARGIN', new_y='NEXT')

        self.ln(10)
        self._font('I', 10)
        self.cell(0, 5.5,
                  'English translation for History vs Hype',
                  align='C', new_x='LMARGIN', new_y='NEXT')

    # ── Legend page ────────────────────────────────────────────

    def legend_page(self):
        self.add_page()
        self.ln(3)

        self._font('', 16)
        self._color(C_HEADING)
        self.cell(0, 10, 'Reading This Document', align='C',
                  new_x='LMARGIN', new_y='NEXT')
        self.ln(3)
        self.thin_rule(width=40)
        self.ln(10)

        self._font('', BODY_SIZE)
        self._color(C_BODY)
        self.multi_cell(0, BODY_LEAD,
            'In October 2010, Serge Klarsfeld announced the discovery of '
            'a five-page typed draft of the Statut des Juifs bearing '
            'Marshal P\u00e9tain\u2019s handwritten annotations. The document, '
            'stamped DOCUMENT CONFIDENTIEL and marked Projet (Draft) in '
            'red pencil, is held at the M\u00e9morial de la Shoah in Paris.',
            align='J')
        self.ln(4)

        self.multi_cell(0, BODY_LEAD,
            'P\u00e9tain\u2019s annotations are concentrated on the first two '
            'pages of the draft, covering the articles that define who is '
            'Jewish and which professions are forbidden. Pages three '
            'through five, containing the media restrictions, transition '
            'provisions, and signatories, bear no significant annotations.',
            align='J')
        self.ln(4)

        self._font('B', BODY_SIZE)
        self.multi_cell(0, BODY_LEAD,
            'Every single handwritten change made the law harsher. '
            'Not one annotation softened it.',
            align='J')
        self.ln(10)

        # Visual conventions section
        self._font('', 14)
        self._color(C_HEADING)
        self.cell(0, 8, 'Visual Conventions', new_x='LMARGIN', new_y='NEXT')
        self.ln(6)

        # Legend items with colored swatches
        items = [
            ('Regular text', 'Typed draft (original text)',
             C_BODY, '', False),
            ('Bold blue text', 'P\u00e9tain\u2019s handwritten additions',
             C_INK, 'B', False),
            ('Red strikethrough', 'Text P\u00e9tain struck out',
             C_STRIKE, '', True),
            ('Gray italic text', 'Translator\u2019s note',
             C_NOTE_TEXT, 'I', False),
        ]

        for label, desc, color, style, strike in items:
            y_start = self.get_y()

            # Color swatch
            self.set_fill_color(*color)
            self.rect(self.l_margin, y_start + 1.5, 4, 4, 'F')
            self.set_fill_color(255, 255, 255)

            # Label
            self.set_x(self.l_margin + 8)
            self._font(style or '', BODY_SIZE)
            self._color(color)
            x_label = self.get_x()
            self.cell(50, 7, label)
            if strike:
                # Draw strikethrough line
                self.set_draw_color(*C_STRIKE)
                self.set_line_width(0.3)
                self.line(x_label, y_start + 3.5,
                          x_label + 48, y_start + 3.5)
                self.set_draw_color(0, 0, 0)

            # Description
            self._font('', BODY_SIZE)
            self._color(C_BODY)
            self.cell(0, 7, f'\u2014  {desc}',
                      new_x='LMARGIN', new_y='NEXT')
            self.ln(3)

        self._color(C_BODY)
        self.ln(8)

        # Numbering note
        self._font('', BODY_SIZE)
        self._color(C_BODY)
        self.multi_cell(0, BODY_LEAD,
            'Article numbers shown in square brackets '
            '[Art. X \u2192 Art. Y] indicate where P\u00e9tain '
            'renumbered the draft articles. The arrow shows the '
            'original draft number and the final published number.',
            align='J')
        self.ln(6)

        # Page structure note
        self._font('I', NOTE_SIZE)
        self._color(C_NOTE_TEXT)
        self.multi_cell(0, 5.5,
            'Note: This translation covers the complete five-page draft. '
            'Pages 1\u20132 contain all of P\u00e9tain\u2019s annotations and are '
            'presented in full detail. Pages 3\u20135 are noted as '
            'unannotated and their content matches the published law.',
            align='J')

    # ── Content helpers ────────────────────────────────────────

    def article_heading(self, text):
        space_left = self.h - self.b_margin - self.get_y()
        if space_left < 50:
            self.add_page()
        self.ln(6)
        self.thin_rule(width=30)
        self.ln(4)
        self._font('', HEADING_SIZE)
        self._color(C_HEADING)
        self.cell(0, 9, text, align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(3)
        self.thin_rule(width=30)
        self.ln(6)

    def draft_page_label(self, text):
        """Label indicating which page of the original draft."""
        self._font('B', 10)
        self._color(C_ACCENT)
        self.cell(0, 6, text, new_x='LMARGIN', new_y='NEXT')
        self._color(C_BODY)
        self.ln(3)

    def typed(self, text):
        """Original typed text (black)."""
        self._font('', BODY_SIZE)
        self._color(C_BODY)
        self.multi_cell(0, BODY_LEAD, text, align='J')
        self.ln(3)

    def typed_indent(self, text, indent=8):
        """Indented typed text for sub-items."""
        self._font('', BODY_SIZE)
        self._color(C_BODY)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent,
                        BODY_LEAD, text, align='J')
        self.ln(2)

    def addition(self, text):
        """Pétain's handwritten addition (bold blue)."""
        self._font('B', BODY_SIZE)
        self._color(C_INK)
        self.multi_cell(0, BODY_LEAD, text, align='J')
        self._color(C_BODY)
        self.ln(3)

    def addition_indent(self, text, indent=8):
        """Indented handwritten addition."""
        self._font('B', BODY_SIZE)
        self._color(C_INK)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent,
                        BODY_LEAD, text, align='J')
        self._color(C_BODY)
        self.ln(2)

    def note(self, text):
        """Translator's note in a subtle background box."""
        y_start = self.get_y()
        usable_w = self.w - self.l_margin - self.r_margin

        # First, measure the height
        self._font('I', NOTE_SIZE)
        h = self.multi_cell(usable_w - 10, 5.5, f'[{text}]',
                            align='J', dry_run=True, output='HEIGHT')

        # Draw background box
        self.set_fill_color(*C_NOTE_BG)
        self.rect(self.l_margin, y_start, usable_w, h + 6, 'F')

        # Draw left accent border
        self._draw_color(C_ANNOT_BORDER)
        self.set_line_width(0.8)
        self.line(self.l_margin, y_start,
                  self.l_margin, y_start + h + 6)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.3)

        # Render text
        self.set_y(y_start + 3)
        self.set_x(self.l_margin + 5)
        self._font('I', NOTE_SIZE)
        self._color(C_NOTE_TEXT)
        self.multi_cell(usable_w - 10, 5.5, f'[{text}]', align='J')
        self._color(C_BODY)
        self.set_fill_color(255, 255, 255)
        self.ln(4)

    def note_inline(self, text):
        """Smaller inline note without background box."""
        self._font('I', NOTE_SIZE)
        self._color(C_NOTE_TEXT)
        indent = 8
        self.set_x(self.l_margin + indent)
        self.multi_cell(
            self.w - self.l_margin - self.r_margin - indent,
            5.5, f'[{text}]', align='J')
        self._color(C_BODY)
        self.ln(2)

    def lettered_item(self, letter, text, struck=False):
        """Lettered list item, optionally with strikethrough."""
        self._font('', BODY_SIZE)
        x = self.get_x()
        indent = 14

        if struck:
            self._color(C_STRIKE)
        else:
            self._color(C_BODY)

        self.cell(indent, BODY_LEAD, f'{letter})', align='R')
        self.set_x(x + indent + 2)
        w = self.w - self.l_margin - self.r_margin - indent - 2
        y_start = self.get_y()
        self.multi_cell(w, BODY_LEAD, text, align='J')
        y_end = self.get_y()

        if struck:
            # Draw strikethrough lines across all rows
            self.set_draw_color(*C_STRIKE)
            self.set_line_width(0.3)
            y = y_start + BODY_LEAD / 2
            while y < y_end:
                self.line(x + indent + 2, y, x + indent + 2 + w, y)
                y += BODY_LEAD
            self.set_draw_color(0, 0, 0)

        self._color(C_BODY)
        self.ln(2)

    def ensure_space(self, mm=55):
        """Add page break if less than mm of space remains."""
        if self.h - self.b_margin - self.get_y() < mm:
            self.add_page()

    def section_break(self):
        self.ln(3)
        self.ornament()
        self.ln(5)


def build_pdf():
    pdf = AnnotatedDraftPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=MARGIN_BOTTOM)
    pdf.set_margins(MARGIN_LR, MARGIN_TOP, MARGIN_LR)
    pdf.setup_fonts()

    # ═══════════════════════════════════════════════════════════
    # TITLE PAGE
    # ═══════════════════════════════════════════════════════════
    pdf.title_page()

    # ═══════════════════════════════════════════════════════════
    # LEGEND PAGE
    # ═══════════════════════════════════════════════════════════
    pdf.legend_page()

    # ═══════════════════════════════════════════════════════════
    # DRAFT PAGE 1 — Articles 1 and 2
    # ═══════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.draft_page_label('DRAFT PAGE 1 OF 5')

    # Draft header markings
    pdf._font('I', 10)
    pdf._color(C_CONF)
    pdf.cell(0, 6, 'DOCUMENT CONFIDENTIEL',
             new_x='LMARGIN', new_y='NEXT')
    pdf._font('I', 10)
    pdf._color(C_ACCENT)
    pdf.cell(0, 6, 'Projet', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(2)

    pdf._font('', 14)
    pdf._color(C_HEADING)
    pdf.cell(0, 9, 'LAW CONCERNING THE STATUS OF JEWS',
             align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(4)

    # ── Article 1 ──
    pdf.article_heading('Article 1')

    pdf.typed(
        'For the application of the present law, any person descended from '
        'three grandparents of the Jewish race, or from two grandparents of '
        'the same race if their spouse is themselves Jewish, is regarded as '
        'Jewish.'
    )

    pdf.note(
        'No annotations by P\u00e9tain on Article 1. The racial '
        'definition\u2014defining Jewishness by grandparents\u2019 '
        '\u201crace\u201d without defining how their race was '
        'determined\u2014was already in the typed draft.'
    )

    # ── Article 2 ──
    pdf.article_heading('Article 2')

    pdf.typed(
        'Access to and exercise of the public functions and offices '
        'enumerated below are forbidden to Jews:'
    )

    # §1 — Judiciary and councils
    pdf.typed_indent(
        'Head of State, Members of the Government, Council of State, '
        'Council of the National Order of the Legion of Honor, Court of '
        'Cassation, Court of Auditors, Corps of Mines, Corps of Bridges '
        'and Roads, General Inspectorate of Finance, Courts of Appeal, '
        'Courts of First Instance and all professional courts,'
    )

    pdf.ensure_space(45)
    pdf.addition_indent('Justices of the Peace,')
    pdf.note(
        'ADDED BY P\u00c9TAIN. Extended the judiciary ban from higher '
        'courts down to the lowest level of local justice\u2014the village '
        'magistrate courts where ordinary French people settled everyday '
        'disputes.'
    )

    pdf.ensure_space(45)
    pdf.addition_indent('all assemblies arising from election;')
    pdf.note(
        'ADDED BY P\u00c9TAIN. The typed draft banned Jews from specific '
        'named institutions. P\u00e9tain\u2019s handwriting added a blanket '
        'ban on ALL elected assemblies\u2014municipal councils, departmental '
        'councils, any elected body whatsoever.'
    )

    # §2 — Civil servants
    pdf.typed_indent(
        'Officials of the Department of Foreign Affairs, '
        'Secretaries-General of ministerial departments, '
        'Directors-General, Directors of central ministry administrations, '
        'Prefects, Sub-Prefects, Secretaries-General of Prefectures, '
        'Inspectors-General of administrative services at the Ministry '
        'of the Interior, civil servants of all grades attached to all '
        'police services;'
    )

    # §3 — Colonial officials
    pdf.typed_indent(
        'Residents-General, Governors-General, Governors and '
        'Secretaries-General of the colonies;'
    )

    pdf.ensure_space(50)
    pdf.addition_indent('colonial inspectorate;')
    pdf.note(
        'ADDED BY P\u00c9TAIN. The typed draft already banned Jews from '
        'governing colonies. P\u00e9tain added the inspectorate\u2014the '
        'officials who oversaw colonial governance. This closed a loophole: '
        'Jews couldn\u2019t govern colonies AND couldn\u2019t inspect how '
        'colonies were governed.'
    )

    # §4 — Education
    pdf.typed_indent(
        'Rectors, Inspectors-General of Public Instruction, Inspectors '
        'of Academy, Headmasters or Directors of secondary and primary '
        'education establishments;'
    )

    pdf.ensure_space(50)
    pdf.addition_indent('all teaching personnel;')
    pdf.note(
        'ADDED BY P\u00c9TAIN. The typed draft listed only specific '
        'educational administrators. P\u00e9tain\u2019s handwriting broadened '
        'this to ALL teaching staff\u2014not just administrators, but every '
        'teacher at every level. In the final law, this became its own '
        'paragraph: \u201cMembers of the teaching corps.\u201d'
    )

    # §5 — Military
    pdf.typed_indent(
        'All officers of the armies of land, sea, and air.'
    )

    # ═══════════════════════════════════════════════════════════
    # DRAFT PAGE 2 — Articles 3→2§6, 4→3, 5→4
    # ═══════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.draft_page_label('DRAFT PAGE 2 OF 5')

    pdf.ensure_space(50)
    pdf.addition(
        '\u2192 P\u00e9tain writes at the top of page 2: '
        '\u201cparagraph 6 of article 2\u201d'
    )
    pdf.note(
        'P\u00e9tain reorganized the structure. What was originally a '
        'separate Article 3 (about state-subsidized enterprises) was '
        'absorbed into Article 2 as paragraph 6, making Article 2 a '
        'single massive article covering ALL professional exclusions.'
    )

    # ── Art. 3 → Art. 2 §6 ──
    pdf.article_heading('[Art. 3 \u2192 Art. 2, \u00a76]')

    pdf.typed(
        'Jews may not hold the functions of administrator, director, or '
        'secretary-general in enterprises receiving concessions or '
        'subsidies from a public authority; they may hold no position '
        'appointed by the Government in enterprises of general interest.'
    )

    pdf.section_break()

    # ── Art. 4 → Art. 3 — THE 1860 CLAUSE ──
    pdf.article_heading('[Art. 4 \u2192 Art. 3]')

    pdf.typed(
        'Access to and exercise of all public functions other than those '
        'enumerated in Articles 2 and 3 are open to Jews only if they can '
        'invoke the following conditions:'
    )

    # The deleted 1860 protection
    pdf.ensure_space(75)
    pdf.lettered_item('a',
        'to be a descendant of Jews born French or naturalized before '
        'the year 1860;',
        struck=True)
    pdf.note(
        'STRUCK OUT BY P\u00c9TAIN. This was a grandfather clause '
        'protecting established French Jewish families\u2014those whose '
        'ancestors had been French citizens since before 1860, predating '
        'the Third Republic. These were families who had been French for '
        '80+ years, fully integrated into French society. In one pen '
        'stroke, P\u00e9tain eliminated the distinction between \u201cold '
        'French Jews\u201d and recent immigrants. The protection that would '
        'have shielded the most assimilated, longest-established Jewish '
        'families in France\u2014gone by P\u00e9tain\u2019s hand. This '
        'clause does NOT appear in the final published law.'
    )

    # Remaining conditions
    pdf.ensure_space(30)
    pdf.lettered_item('b',
        'to have been cited during the 1914\u20131918 campaign or at least '
        'to hold the Veteran\u2019s Card of 1914\u20131918;')
    pdf.note_inline('Kept. Became final Article 3, condition (a).')

    pdf.ensure_space(30)
    pdf.lettered_item('c',
        'to have been cited in dispatches during the 1939\u20131940 '
        'campaign;')
    pdf.note_inline('Kept. Became final Article 3, condition (b).')

    pdf.ensure_space(40)
    pdf.lettered_item('d',
        'to be decorated with the Legion of Honor for military service '
        'or with the Military Medal.')
    pdf.note(
        'Kept. Became final Article 3, condition (c). P\u00e9tain added '
        '\u201cde guerre\u201d (wartime)\u2014narrowing the exception to '
        'wartime decorations only, excluding peacetime honors.'
    )

    pdf.section_break()

    # ── Art. 5 → Art. 4 ──
    pdf.article_heading('[Art. 5 \u2192 Art. 4]')

    pdf.typed(
        'Access to and exercise of the liberal professions, independent '
        'professions, functions assigned to ministerial officers and to all '
        'auxiliaries of justice are permitted to Jews in a proportion fixed, '
        'for each category, by public administrative regulations.'
    )

    pdf.addition(
        'P\u00e9tain adds between the lines: \u201cif there is reason '
        'to\u201d\u2014modifying the quota system to make it more restrictive.'
    )

    pdf.typed(
        'In the professions listed above, special regulations shall '
        'determine the conditions under which the elimination of Jews in '
        'excess numbers shall take place.'
    )

    # ═══════════════════════════════════════════════════════════
    # DRAFT PAGES 3–5 — Remaining articles (no annotations)
    # ═══════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.draft_page_label('DRAFT PAGES 3\u20135 OF 5')

    pdf._font('', BODY_SIZE)
    pdf._color(C_BODY)
    pdf.multi_cell(0, BODY_LEAD,
        'The remaining three pages of the typed draft contain Articles '
        '5 through 10 of the law as published. These pages bear no '
        'significant handwritten annotations by P\u00e9tain. The text '
        'on these pages matches the version published in the Journal '
        'Officiel of October 18, 1940.',
        align='J')
    pdf.ln(4)

    pdf.multi_cell(0, BODY_LEAD,
        'For the complete translated text of these articles, see the '
        'companion document: Law of October 3, 1940, Concerning the '
        'Status of Jews (English Translation).',
        align='J')
    pdf.ln(6)

    # Brief summary of unannotated articles
    pdf._font('', 13)
    pdf._color(C_HEADING)
    pdf.cell(0, 8, 'Summary of Unannotated Articles',
             new_x='LMARGIN', new_y='NEXT')
    pdf.ln(4)

    unannotated = [
        ('Article 5 (Draft page 3)',
         'Total ban on Jews in media: newspapers, magazines, cinema, '
         'theater, and radio broadcasting. No exceptions.'),
        ('Article 6 (Draft page 3)',
         'Jews banned from all professional governing bodies and '
         'disciplinary boards.'),
        ('Article 7 (Draft page 4)',
         'Jewish civil servants must leave within two months of '
         'publication. Pension provisions for orderly removal.'),
        ('Article 8 (Draft page 4)',
         'Individual exemptions possible for Jews who rendered '
         '\u201cexceptional services\u201d in literature, science, or '
         'art. Discretionary, not automatic.'),
        ('Article 9 (Draft page 4)',
         'Law applies to Algeria, all colonies, protectorates, and '
         'mandated territories\u2014the entire French empire.'),
        ('Article 10 and signatories (Draft page 5)',
         'Publication clause. Signed by P\u00e9tain and nine ministers '
         'of the Vichy cabinet.'),
    ]

    for heading, desc in unannotated:
        pdf._font('B', BODY_SIZE)
        pdf._color(C_BODY)
        pdf.cell(0, BODY_LEAD, heading, new_x='LMARGIN', new_y='NEXT')
        pdf._font('', BODY_SIZE)
        pdf.multi_cell(0, BODY_LEAD, desc, align='J')
        pdf.ln(3)

    # ═══════════════════════════════════════════════════════════
    # SUMMARY OF PÉTAIN'S ANNOTATIONS
    # ═══════════════════════════════════════════════════════════
    pdf.add_page()

    pdf._font('', 16)
    pdf._color(C_HEADING)
    pdf.cell(0, 10, 'Summary of P\u00e9tain\u2019s Annotations',
             align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)
    pdf.thin_rule(width=40)
    pdf.ln(8)

    pdf._font('B', BODY_SIZE)
    pdf._color(C_BODY)
    pdf.cell(0, BODY_LEAD, 'Every change made the law harsher.',
             new_x='LMARGIN', new_y='NEXT')
    pdf._font('', BODY_SIZE)
    pdf.cell(0, BODY_LEAD, 'Not a single annotation softened it.',
             new_x='LMARGIN', new_y='NEXT')
    pdf.ln(8)

    # Summary table
    changes = [
        ('1', 'Added \u201cJustices of the Peace\u201d',
         'Extended judiciary ban to lowest courts', True),
        ('2', 'Added \u201call assemblies arising from election\u201d',
         'Blanket ban on all elected office', True),
        ('3', 'Added \u201ccolonial inspectorate\u201d',
         'Closed colonial governance loophole', True),
        ('4', 'Added \u201call teaching personnel\u201d',
         'From administrators to ALL teachers', True),
        ('5', 'Reorganized Art. 3 \u2192 Art. 2 \u00a76',
         'Single comprehensive exclusion article', False),
        ('6', 'Struck out the 1860 protection',
         'Removed protection for established French Jewish families', True),
        ('7', 'Added \u201cde guerre\u201d qualifier',
         'Narrowed military exception to wartime only', True),
        ('8', 'Modified quota language (Art. 5 \u2192 4)',
         'Strengthened enforcement of professional quotas', True),
    ]

    for num, change, effect, is_harsher in changes:
        # Number + change
        pdf._font('B', 11)
        pdf._color(C_BODY)
        pdf.cell(8, 7, f'{num}.')
        pdf._font('', 11)
        pdf.cell(0, 7, f'  {change}', new_x='LMARGIN', new_y='NEXT')

        # Effect + direction label
        pdf._font('I', 10)
        pdf._color(C_NOTE_TEXT)
        pdf.cell(8, 6, '')

        direction_w = 30
        effect_w = (pdf.w - pdf.l_margin - pdf.r_margin
                    - 8 - direction_w)

        pdf.cell(effect_w, 6, f'  {effect}')

        if is_harsher:
            pdf._color(C_STRIKE)
            pdf._font('B', 9)
            pdf.cell(direction_w, 6, 'HARSHER', align='R',
                     new_x='LMARGIN', new_y='NEXT')
        else:
            pdf._color(C_NOTE_TEXT)
            pdf._font('B', 9)
            pdf.cell(direction_w, 6, 'STRUCTURAL', align='R',
                     new_x='LMARGIN', new_y='NEXT')

        pdf._color(C_BODY)
        pdf.ln(3)

    # ═══════════════════════════════════════════════════════════
    # COLOPHON
    # ═══════════════════════════════════════════════════════════
    pdf.ln(6)
    pdf.ornament()
    pdf.ln(8)

    pdf._font('I', 9.5)
    pdf._color(C_NOTE_TEXT)
    pdf.multi_cell(0, 5.2,
        'This annotated translation is based on the five-page typed '
        'draft with handwritten annotations discovered by Serge '
        'Klarsfeld, announced October 3, 2010, at the M\u00e9morial de '
        'la Shoah, Paris. The handwriting has been confirmed as '
        'P\u00e9tain\u2019s. Annotations are documented following '
        'Klarsfeld\u2019s analysis and confirmed against the published '
        'text in the Journal Officiel de la R\u00e9publique Fran\u00e7aise, '
        'No. 266, October 18, 1940.',
        align='J')

    pdf.ln(8)
    pdf._font('I', 9)
    pdf._color(C_FOOTER)
    pdf.cell(0, 5, 'History vs Hype', align='C')

    # ── Save ───────────────────────────────────────────────────
    out = OUTPUT_DIR / 'ANNOTATED-DRAFT-Statut-des-Juifs-1940.pdf'
    pdf.output(str(out))
    print(f'PDF saved to: {out}')
    return out


if __name__ == '__main__':
    build_pdf()
