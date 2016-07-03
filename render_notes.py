# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

# test html:
content = """
<annotations class="md-whiteframe-z2 ng-scope">
  <h3>Notes</h3>

  <!-- ngIf: !annots.length --><div ng-if="!annots.length" class="ng-scope">
    <h4>You have no notes.</h4>
    <div class="tip">
      Tip: To annotate, select any text in the article to get the annotation menu. You can add highlights and comments, which will be listed here in this panel.
    </div>
  </div><!-- end ngIf: !annots.length -->

  <!-- ngIf: annots.length -->

  <!-- ngIf: annots.length -->
  <button class="md-icon-button close md-button md-ink-ripple" ng-transclude="" ng-click="toggleAnnots()">
    <i class="material-icons ng-scope">close</i>
  </button>
</annotations>
"""

content2 = """<annotations class="md-whiteframe-z2 ng-scope">
  <h3>Notes</h3>

  <!-- ngIf: !annots.length -->

  <!-- ngIf: annots.length --><div ng-if="annots.length" class="ng-scope">
    <div class="sort-options layout-row">
      <md-input-container class="sort-order md-input-has-value">
        <label for="select_3" class="md-static">Order by:</label>
        <md-select ng-model="sortPredicate" class="ng-pristine ng-untouched ng-valid ng-not-empty" tabindex="0" aria-disabled="false" role="combobox" aria-expanded="false" id="select_3" aria-invalid="false" aria-label="Order by:"><md-select-value class="md-select-value" id="select_value_label_0"><span>position</span><span class="md-select-icon" aria-hidden="true"></span></md-select-value></md-select>
      </md-input-container>
      <md-input-container class="sort-direction md-input-has-value">
        <label for="select_5" class="md-static">Direction:</label>
        <md-select ng-model="sortDirection" class="ng-pristine ng-untouched ng-valid ng-not-empty" tabindex="0" aria-disabled="false" role="combobox" aria-expanded="false" id="select_5" aria-invalid="false" aria-label="Direction:"><md-select-value class="md-select-value" id="select_value_label_1"><span>descending</span><span class="md-select-icon" aria-hidden="true"></span></md-select-value></md-select>
      </md-input-container>
    </div>
    <!-- ngRepeat: annot in annots | orderBy:predicates[sortPredicate]:directions[sortDirection] --><div class="note-item ng-scope" ng-click="scrollTo(annot)" ng-repeat="annot in annots | orderBy:predicates[sortPredicate]:directions[sortDirection]" role="button" tabindex="0">
      <!-- ngIf: sortPredicate == 'created' -->
      <!-- ngIf: sortPredicate != 'created' --><div ng-if="sortPredicate != 'created'" class="note-time-date ng-binding ng-scope">
        Last Tuesday at 9:49 PM
      </div><!-- end ngIf: sortPredicate != 'created' -->
      <div class="note-highlight ng-binding color-1" ng-class="'color-' + annot.color_id">The ergogenic effects of caffeine on athletic performance have been shown in many studies, and its broad range of metabolic, hormonal, and physiologic effects has been recorded, as this review of the literature shows. </div>
      <!-- ngIf: annot.note -->
    </div><!-- end ngRepeat: annot in annots | orderBy:predicates[sortPredicate]:directions[sortDirection] --><div class="note-item ng-scope" ng-click="scrollTo(annot)" ng-repeat="annot in annots | orderBy:predicates[sortPredicate]:directions[sortDirection]" role="button" tabindex="0">
      <!-- ngIf: sortPredicate == 'created' -->
      <!-- ngIf: sortPredicate != 'created' --><div ng-if="sortPredicate != 'created'" class="note-time-date ng-binding ng-scope">
        Today at 3:43 PM
      </div><!-- end ngIf: sortPredicate != 'created' -->
      <div class="note-highlight ng-binding color-2" ng-class="'color-' + annot.color_id">to 4 days after caffeine cessation when a placebo was given; however, acute caffeine ingestion after 2 to 4 days of cessation resulted in </div>
      <!-- ngIf: annot.note -->
    </div><!-- end ngRepeat: annot in annots | orderBy:predicates[sortPredicate]:directions[sortDirection] -->
  </div><!-- end ngIf: annots.length -->

  <!-- ngIf: annots.length --><button class="md-icon-button download md-button ng-scope md-ink-ripple ng-animate ng-enter ng-enter-active" ng-transclude="" ng-if="annots.length" ng-click="downloadAnnots()" data-ng-animate="2">
    <i class="material-icons ng-scope">file_download</i>

  </button><!-- end ngIf: annots.length -->
  <button class="md-icon-button close md-button md-ink-ripple" ng-transclude="" ng-click="toggleAnnots()">
    <i class="material-icons ng-scope">close</i>
  </button>
</annotations>"""

content3 = """<annotations class="md-whiteframe-z2 ng-scope">
  <h3>Notes</h3>

  <!-- ngIf: !annots.length -->

  <!-- ngIf: annots.length --><div ng-if="annots.length" class="ng-scope">
    <div class="sort-options layout-row">
      <md-input-container class="sort-order md-input-has-value">
        <label for="select_3" class="md-static">Order by:</label>
        <md-select ng-model="sortPredicate" class="ng-pristine ng-untouched ng-valid ng-not-empty" tabindex="0" aria-disabled="false" role="combobox" aria-expanded="false" id="select_3" aria-invalid="false" aria-label="Order by:"><md-select-value class="md-select-value" id="select_value_label_0"><span>position</span><span class="md-select-icon" aria-hidden="true"></span></md-select-value></md-select>
      </md-input-container>
      <md-input-container class="sort-direction md-input-has-value">
        <label for="select_5" class="md-static">Direction:</label>
        <md-select ng-model="sortDirection" class="ng-pristine ng-untouched ng-valid ng-not-empty" tabindex="0" aria-disabled="false" role="combobox" aria-expanded="false" id="select_5" aria-invalid="false" aria-label="Direction:"><md-select-value class="md-select-value" id="select_value_label_1"><span>descending</span><span class="md-select-icon" aria-hidden="true"></span></md-select-value></md-select>
      </md-input-container>
    </div>
    <!-- ngRepeat: annot in annots | orderBy:predicates[sortPredicate]:directions[sortDirection] --><div class="note-item ng-scope" ng-click="scrollTo(annot)" ng-repeat="annot in annots | orderBy:predicates[sortPredicate]:directions[sortDirection]" role="button" tabindex="0">
      <!-- ngIf: sortPredicate == 'created' -->
      <!-- ngIf: sortPredicate != 'created' --><div ng-if="sortPredicate != 'created'" class="note-time-date ng-binding ng-scope">
        Last Tuesday at 9:49 PM
      </div><!-- end ngIf: sortPredicate != 'created' -->
      <div class="note-highlight ng-binding color-1" ng-class="'color-' + annot.color_id">The ergogenic effects of caffeine on athletic performance have been shown in many studies, and its broad range of metabolic, hormonal, and physiologic effects has been recorded, as this review of the literature shows. </div>
      <!-- ngIf: annot.note -->
    </div><!-- end ngRepeat: annot in annots | orderBy:predicates[sortPredicate]:directions[sortDirection] --><div class="note-item ng-scope" ng-click="scrollTo(annot)" ng-repeat="annot in annots | orderBy:predicates[sortPredicate]:directions[sortDirection]" role="button" tabindex="0">
      <!-- ngIf: sortPredicate == 'created' -->
      <!-- ngIf: sortPredicate != 'created' --><div ng-if="sortPredicate != 'created'" class="note-time-date ng-binding ng-scope">
        Today at 7:26 PM
      </div><!-- end ngIf: sortPredicate != 'created' -->
      <div class="note-highlight ng-binding color-1" ng-class="'color-' + annot.color_id">before performance can provide the same ergogenic effects as acute intake; caffeine can be taken gradually at low doses to avoid tolerance during the course of 3 or 4 days, just before</div>
      <!-- ngIf: annot.note --><div class="note-text ng-binding ng-scope" ng-if="annot.note">test note test note test note
</div><!-- end ngIf: annot.note -->
    </div><!-- end ngRepeat: annot in annots | orderBy:predicates[sortPredicate]:directions[sortDirection] --><div class="note-item ng-scope" ng-click="scrollTo(annot)" ng-repeat="annot in annots | orderBy:predicates[sortPredicate]:directions[sortDirection]" role="button" tabindex="0">
      <!-- ngIf: sortPredicate == 'created' -->
      <!-- ngIf: sortPredicate != 'created' --><div ng-if="sortPredicate != 'created'" class="note-time-date ng-binding ng-scope">
        Today at 3:43 PM
      </div><!-- end ngIf: sortPredicate != 'created' -->
      <div class="note-highlight ng-binding color-2" ng-class="'color-' + annot.color_id">to 4 days after caffeine cessation when a placebo was given; however, acute caffeine ingestion after 2 to 4 days of cessation resulted in </div>
      <!-- ngIf: annot.note -->
    </div><!-- end ngRepeat: annot in annots | orderBy:predicates[sortPredicate]:directions[sortDirection] -->
  </div><!-- end ngIf: annots.length -->

  <!-- ngIf: annots.length --><button class="md-icon-button download md-button ng-scope md-ink-ripple" ng-transclude="" ng-if="annots.length" ng-click="downloadAnnots()" style="">
    <i class="material-icons ng-scope">file_download</i>

  </button><!-- end ngIf: annots.length -->
  <button class="md-icon-button close md-button md-ink-ripple" ng-transclude="" ng-click="toggleAnnots()">
    <i class="material-icons ng-scope">close</i>
  </button>
</annotations>"""

# html bodies:
main_body = """<style type="text/css">
.lined_box_1 {
    border-left: 7px solid #fff94b;
    padding-left: 12px;
}
.lined_box_2 {
    border-left: 7px solid #90ee90;
    padding-left: 12px;
}
.lined_box_3 {
    border-left: 7px solid #ffb6c1;
    padding-left: 12px;
}
.lined_box_4 {
    border-left: 7px solid #8E4585;
    padding-left: 12px;
}
</style>

"""
note_body = """<div class="lined_box_{}">
<p><em><span style="font-size:16px;"><strong><span style="font-size:18px;"><u>{}</u></span></strong></span></em></p>
<em><span style="font-size:16px;">{}</span></em></div>
"""
bold_body = """<p><span style="font-size:16px;"><strong>{}</strong></span></p><p></p>"""
p_taq = "<p></p>"


def extract_notes(source):
    soup = BeautifulSoup(source, 'lxml')
    outer_divs = soup.find_all("div", {"class": "note-item ng-scope"})

    item_list = []

    pat = re.compile(r'(?<=color-)\d')

    for o in outer_divs:
        color = re.findall(pat, str(o))[0]
        x = o.get_text('|||', strip=True).split('|||')  # unelegant, but it works
        item_list.append([color] + x)

    return item_list


def render_notes(source):
    data_list = extract_notes(source)
    note_items = ''
    for o in data_list:
        note_items += note_body.format(o[0], o[1], o[2])
        if len(o) == 4:
            note_items += bold_body.format(o[3])
        else:
            note_items += p_taq

    full_body = main_body + note_items
    return full_body


### ------------------------------------------------




# print render_notes(content3)
#
# driver = webdriver.Chrome()
# driver.get("data:text/html;charset=utf-8," + render_notes(item_list))
