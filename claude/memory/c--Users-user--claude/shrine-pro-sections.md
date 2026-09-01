# Shrine Pro Theme — Sections Reference
Tema: Farma Vive (afarmavive.myshopify.com)
Arquivo tema: theme_export__afarmavive-shop-theme-export-reliviaessential-online-shrine-pr__26FEB2026-0555pm
Seções: C:/Users/user/Downloads/[pasta-do-tema]/sections/

---

## NOTAS GERAIS

### Color Schemes disponíveis (padrão em todas as seções):
- `accent-1` — cor roxa (#6d388b)
- `accent-2`
- `background-1` — fundo claro padrão
- `background-2`
- `inverse`
- `custom` — ativa custom_colors_* settings

### Para usar cores customizadas:
Definir `color_scheme: "custom"` (ou `section_color_scheme: "custom"`) E setar os campos:
- `custom_colors_background` — cor de fundo
- `custom_colors_text` — cor do texto
- `custom_colors_solid_button_background` — botão sólido bg
- `custom_colors_solid_button_text` — botão sólido texto
- `custom_colors_outline_button` — botão outline
- `custom_gradient_background` — gradiente (opcional)

### Farma Vive brand colors:
- Purple accent: `#6d388b`
- Stars: `#ffcc00`
- CTA button: `#dd1d1d`
- Dark bg: `#2e2a39`

---

## SEÇÕES PARA PÁGINAS DE PRODUTO

### main-product
**Tipo:** `main-product`
**Uso:** Seção principal do produto — obrigatória em templates de produto.
**Settings principais:** `media_position` (left/right), `gallery_layout` (thumbnail_slider/stacked/...), `enable_sticky_info`

**Block Types disponíveis:**
- `title` — settings: `text_size`(h0/h1/h2), `title_alignment`(left/center), `uppercase_title`(bool)
- `review_avatars` — settings: avatars 1-5 (image_picker), avatar_N_verified(bool), `star_color`, `checkmark_color`, `stars_label`(inline_richtext), `alignment`, `avatar_size`, `stars_scroll_id`
- `rating_stars` — settings: `rating`, `star_color`, `label`, `scroll_id`
- `trustpilot_stars` — settings: `rating`, `star_color`, `label`, `scroll_id`
- `price` — configurações de exibição de preço
- `description` — exibe descrição do produto
- `variant_picker` — settings: `picker_types`(pills/dropdown/swatches/quantity breaks/hidden), `breaks_headline`, `breaks_color_scheme`, `breaks_benefits`, `skip_unavailable`
- `buy_buttons` — settings: `show_dynamic_checkout`, `skip_cart`, `uppercase_text`, `enable_custom_color`, `custom_color`, `enable_secondary_btn`, `secondary_btn_label`
- `urgency` — settings: `urgency`(text), `color_scheme`
- `sticky_atc` — settings: `function`, `display_when`, `button_label`, `color_scheme`, `enable_custom_btn_color`, `custom_btn_color`, `desktop_show_price`, `desktop_variant_picker`, `mobile_full_button_width`, `stars_label`
- `collapsible_tab` — accordion interno na página de produto
- `image` — imagem adicional no bloco de info
- `divider` — separador visual
- `payment_badges` — selos de pagamento
- `emoji_benefits` — lista de benefícios com emojis
- `bundle_offer` — oferta de bundle
- `estimated_shipping` — prazo de entrega estimado
- `scroll_buttons` — botões de scroll para outras seções
- `sku`, `inventory`, `share`, `rating`, `complementary`, `sizing_chart`, `popup`, `custom_liquid`, `@app`

---

### image-with-text
**Tipo:** `image-with-text`
**Uso:** Seção de imagem + texto lado a lado. Muito versátil.
**Settings principais:**
- `image`(image_picker), `video`(video), `video_autoplay`(bool), `video_loop`(bool)
- `height`: adapt/small/medium/large
- `layout`: image_first / text_first
- `desktop_media_width`: 25–75%
- `desktop_content_position`: top/middle/bottom
- `desktop_content_alignment`: left/center/right
- `content_layout`: no-overlap/overlap
- `color_scheme`, `section_color_scheme` (ambos aceitam "custom")
- `custom_colors_background`, `custom_colors_text`, `custom_colors_solid_button_background`, etc.
- `desktop_padding_top`, `desktop_padding_bottom`, `mobile_padding_top`, `mobile_padding_bottom`
- `mobile_direction`: normal(media first) / reverse(media second)

**Block Types:**
- `heading` — `title`(inline_richtext), `title_highlight_color`(color), `heading_size`(h0/h1/h2)
- `caption` — `caption`(text), `text_style`(subtitle/caption-with-letter-spacing), `text_size`(small/medium/large)
- `text` — `text`(richtext), `text_style`(body/subtitle)
- `text_with_icon` — `text_1/2/3`(inline_richtext), `icon_1/2/3`(text=Material Symbol name), `filled_icon_1/2/3`, `custom_icon_1/2/3`(image_picker), `direction`(horizontal/vertical), `icon_color`, `text_color`, `enable_bg`, `bg_color`
- `image` — `image`(image_picker), `width`(0-100%), `alignment`, `border_radius`
- `button` — `button_label`, `button_link`, `button_style_secondary`(bool)
- `atc_button` — `button_label`, `atc_product`(product), `atc_skip_cart`
- `rating_stars` — `rating`, `star_color`, `bg_star_color`, `label`, `size`, `scroll_id`
- `trustpilot_stars` — `rating`, `star_color`, `bg_star_color`, `star_symbol_color`, `label`, `size`, `scroll_id`

---

### rich-text
**Tipo:** `rich-text`
**Uso:** Seção de texto rico centralizado, sem imagem. Boa para stats, citações, CTAs.
**Settings principais:**
- `desktop_content_position`: left/center/right
- `content_alignment`: left/center/right
- `full_width`: bool
- `color_scheme` (aceita "custom")
- `padding_top`, `padding_bottom`
- `custom_colors_background`, `custom_colors_text`, etc.

**Block Types:**
- `heading` — `title`(inline_richtext), `title_highlight_color`, `heading_size`(h0/h1/h2)
- `caption` — `caption`(text), `text_style`, `text_size`
- `text` — `text`(richtext)
- `button` — `button_label`, `button_link`, `button_style_secondary`, `button_label_2`, `button_link_2`, `button_style_secondary_2`
- `atc_button` — `button_label`, `atc_product`, `atc_skip_cart`
- `rating_stars` — `rating`, `star_color`, `bg_star_color`, `bg_stars_style`, `label`, `size`, `scroll_id`
- `trustpilot_stars` — `rating`, `star_color`, `bg_star_color`, `star_symbol_color`, `label`, `size`, `scroll_id`

---

### collapsible-content
**Tipo:** `collapsible-content`
**Uso:** FAQ, especificações, accordions. Pode ter imagem lateral.
**Settings principais:**
- `title`(inline_richtext), `title_highlight_color`, `heading_size`, `heading_alignment`
- `caption`(text)
- `layout`: none/left/right (posição da imagem)
- `desktop_layout`: collapse_last / collapse_first
- `image`(image_picker), `video`(video)
- `image_ratio`: adapt/square/portrait/landscape
- `color_scheme`, `container_color_scheme` (ambos aceitam "custom")
- `open_first_collapsible_row`: bool
- `row_heading_size`: small/medium/large
- `collapse_icon`: plus/arrow
- `display_top_border`: bool
- `padding_top`, `padding_bottom`
- `custom_colors_background`, `custom_gradient_background`, `custom_colors_text`
- `custom_contaner_colors_background`, `custom_container_gradient_background`, `custom_contaner_colors_text`

**Block Types:**
- `collapsible_row` — `heading`(text), `icon`(text=Material Symbol), `filled_icon`(bool), `custom_icon`(image_picker), `row_content`(richtext), `page`(page)

---

### multirow
**Tipo:** `multirow`
**Uso:** Seção de múltiplas linhas imagem+texto alternadas. Ideal para "Como Funciona".
**Settings principais:**
- `image_height`: adapt/small/medium/large
- `desktop_image_width`: small/medium/large/x-large
- `heading_size`, `text_style`, `button_style`
- `desktop_content_position`: top/middle/bottom
- `desktop_content_alignment`: left/center/right
- `image_layout`: none/alternate-left/alternate-right
- `row_color_scheme`, `section_color_scheme` (ambos aceitam "custom")
- `mobile_direction`: normal/reverse
- `padding_top`, `padding_bottom`
- `custom_colors_background`, `custom_gradient_background`, `custom_colors_text`, etc.

**Block Types:**
- `row` — `image`(image_picker), `video`(video), `video_muted_autoplay`(bool), `caption`(text), `title`(inline_richtext), `title_highlight_color`(color), `text`(richtext), `button_label`, `button_link`, `atc_button_label`, `atc_product`, `atc_skip_cart`

---

### testimonials
**Tipo:** `testimonials`
**Uso:** Grid ou slider de depoimentos.
**Settings principais:**
- `title`(inline_richtext), `title_highlight_color`, `heading_size`
- `text`(richtext) — subtítulo da seção
- `color_scheme` (aceita "custom")
- `image_width`: small/standard/large/circle
- `image_ratio`: adapt/square/portrait
- `column_alignment`: left/center/right
- `show_stars`: bool, `star_color`, `bg_star_color`, `inactive_stars_style`
- `show_quotes`: bool, `quotes_color_scheme`
- `cards_color_scheme` (aceita "custom")
- `type`: grid/slider
- `autoplay`, `autoplay_speed`
- `columns_desktop`: 1-6
- `slider_desktop`, `per_move_desktop`, `desktop_spacing`
- `slider_mobile`, `enable_mobile_preview`
- `padding_top`, `padding_bottom`
- `custom_colors_background`, `custom_cards_colors_background`, etc.

**Block Types:**
- `column` — `image`(image_picker), `video`(video), `video_thumbnail`(image_picker), `star_rating`(range 0-5), `title`(text), `text`(richtext), `author_avatar`(image_picker), `author`(inline_richtext)

---

### section-divider
**Tipo:** `section-divider`
**Uso:** Divisor visual entre seções (ondas, triângulos, etc.)
**Settings:**
- `visibility`: always-display/desktop-hidden/mobile-hidden
- `shape`: waves/waves_3/triangle/tilt/curve (verificar opções reais no tema)
- `flip_horizontal`: bool
- `flip_vertical`: bool
- `shape_color`: accent-1/accent-2/background-1/background-2/inverse/custom
- `custom_shape_color`(color)
- `background_color`: accent-1/accent-2/background-1/background-2/inverse/custom
- `custom_background_color`(color)
- `padding_top`, `padding_bottom`
**Blocks:** Nenhum

---

### multicolumn
**Tipo:** `multicolumn`
**Uso:** Grid de colunas com imagem, título, texto. Bom para features/benefícios.
**Settings principais:**
- `title`(inline_richtext), `title_highlight_color`, `heading_size`
- `button_label`, `button_link` (botão da seção)
- `color_scheme`, `cards_color_scheme` (ambos aceitam "custom")
- `cards_corner_radius`, `stretch_cards`
- `image_width`, `image_ratio`, `media_position`
- `column_alignment`: left/center/right
- `columns_desktop`: 1-6
- `type`: grid/slider, `autoplay`, `slider_desktop`, etc.
- `padding_top`, `padding_bottom`

**Block Types:**
- `column` — `image`(image_picker), `video`(video), `video_thumbnail`(image_picker), `muted_autoplay`(bool), `title`(text), `text`(richtext), `link_label`, `link`(url)

---

### product-features
**Tipo:** `product-features`
**Uso:** Imagem com hotspots clicáveis ou bullet points. Ideal para destacar features.
**Settings principais:**
- `title`(inline_richtext), `title_highlight_color`, `heading_size`
- `text`(richtext), `button_label`, `link`, `atc_button_label`
- `image`(image_picker), `mobile_image`(image_picker)
- `desktop_image_width`: small/medium/large/x-large
- `full_page_width`, `image_corner_radius`, `content_corner_radius`
- `color_scheme`, `section_color_scheme`
- `hotspot_open_event`, `hotspots_color_scheme`, `display_hotspots_animation`, `hotspot_content_color_scheme`
- `bullet_points_color`, `contain_bullet_points`
- `desktop_content_position`, `desktop_content_alignment`
- `padding_top`, `padding_bottom`

**Block Types:**
- `hotspot` — `offset_x/y`(range), `mobile_offset_x/y`, `image`, `title`, `text`, `alignment`
- `bullet_point` — `offset_x/y`, `direction`, `line_bend`, mobile equivalents, `title`, `text`

---

### icons-with-content
**Tipo:** `icons-with-content`
**Uso:** Lista de ícones com texto. Bom para benefits/features resumidos.
**Settings principais:**
- `color_scheme` (aceita "custom")
- `icon_size`: small/medium/large/x-large
- `icon_position`: left/top
- `icon_color`: accent-1/accent-2/background-1/etc
- `icon_heading_size`, `icon_text_alignment`
- `icons_desktop_layout`: 1-4 colunas
- `icons_mobile_layout`
- `layout`, `mobile_layout` (da seção completa)
- `padding_top`, `padding_bottom`

**Block Types:**
- `icon` — `icon`(text=Material Symbol name), `filled_icon`(bool), `image`(image_picker), `title`(text), `text`(richtext)
- `heading` — `title`(inline_richtext), `title_highlight_color`, `heading_size`
- `caption`, `text`, `button`, `atc_button`, `image`, `video`

---

### content-tabs
**Tipo:** `content-tabs`
**Uso:** Abas clicáveis com conteúdo diferente em cada aba. Ótimo para variantes, comparações.
**Settings principais:**
- `title`(inline_richtext), `title_highlight_color`, `heading_size`
- `text`(richtext)
- `color_scheme` (aceita "custom")
- `container_width`, `buttons_color_scheme`, `button_border_radius`, `buttons_style`
- `active_button_animation`, `header_layout`
- `padding_top`, `padding_bottom`

**Block Types:**
- `tab` — `btn_label`(inline_richtext), `btn_icon`(text), `filled_btn_icon`(bool), `image`(image_picker), `video`(video), `title`(inline_richtext), `title_highlight_color`, `heading_size`, `text`(richtext), `button_label`, `link`, `atc_button_label`, `desktop_media_width`, `desktop_media_position`, `desktop_text_alignment`, `mobile_media_position`, `mobile_text_alignment`

---

### comparison-table
**Tipo:** `comparison-table`
**Uso:** Tabela comparativa produto X concorrentes.
**Settings principais:**
- `title`, `text`, `button_label`, `link`, `atc_button_label`
- `color_scheme`, `layout`, `style`, `corner_radius`
- `number_of_competitors`: 1-3
- `us_label`, `logo`(image_picker), `logo_width`
- `others_label`, `others_logo`, etc. (até others_3)
- `checkmark_style`, `checkmark_color`, `checkmark_bg_color`
- `x_style`, `x_color`, `x_bg_color`
- `highlighted_color_scheme`, `other_cells_color_scheme`
- `padding_top`, `padding_bottom`

**Block Types:**
- `row` — `benefit`(inline_richtext), `us`(bool), `others`(bool), `others_2`(bool), `others_3`(bool)

---

### image-banner
**Tipo:** `image-banner`
**Uso:** Banner/hero com imagem de fundo e texto sobreposto.
**Settings principais:**
- `image`(image_picker), `image_2`(image_picker — mobile)
- `image_overlay_opacity`: 0-100
- `image_height`: adapt/small/medium/large/full_screen
- `desktop_content_position`, `desktop_content_alignment`
- `color_scheme`, `show_text_box`, `transparent_container_color`
- `mobile_content_alignment`, `stack_images_on_mobile`, `show_text_below`

**Block Types:**
- `heading` — `title`, `title_highlight_color`, `heading_size`
- `text` — `text`(text), `text_style`
- `buttons` — `button_label_1`, `button_link_1`, `button_style_secondary_1`, `button_label_2`, `button_link_2`, `button_style_secondary_2`
- `atc_button` — `button_label`, `atc_product`, `atc_skip_cart`
- `rating_stars`, `trustpilot_stars`

---

### parallax-hero
**Tipo:** `parallax-hero`
**Uso:** Hero com efeito parallax 3D ao fazer scroll.
**Settings principais:**
- `desktop_bg_image`, `desktop_bg_video`, `mobile_bg_image`, `mobile_bg_video`
- `overlay_color`, `overlay_opacity`
- `min_desktop_height_type`, `desktop_pixels_height`
- `transparent_header`
- `padding_top`, `padding_bottom`

**Block Types:**
- `content` — `heading`, `title_highlight_color`, `heading_size`, `text`, buttons, `color_scheme`, layout settings, scroll speed/zoom/rotation settings
- `image` — `desktop_image`, `mobile_image`, scroll speed/zoom/rotation settings

---

### pricing-table
**Tipo:** `pricing-table`
**Uso:** Tabela de planos/preços. Excelente para quantity breaks visuais.
**Settings principais:**
- `title`, `text`, `icon_size`, `color_scheme`
- `desktop_spacing`, `cards_alignment`
- `padding_top`, `padding_bottom`

**Block Types:**
- `plan` — `product`(product), `variant_index`(number), `card_style`, `color_scheme`, `badge`(text), `badge_color_scheme`, `title`, `price`, `price_text`, `icon`(text), `custom_icon`(image_picker), `description`, `benefits`(richtext), `button_function`, `button_label`, `link`, `button_style_secondary`, `button_full_width`, cores customizadas

---

### bundle-deals
**Tipo:** `bundle-deals`
**Uso:** Ofertas de bundles com múltiplos produtos.
**Settings principais:**
- `title`, `text`, `color_scheme`, `layout`
- `enable_price_changes`, `skip_unavailable`, `prices_under`, `skip_cart`
- `total_price_label`, `btn_label`
- `percentage_discount`, `fixed_amount_discount`
- `padding_top`, `padding_bottom`

**Block Types:**
- `product` — `product`(product), `percentage_discount`(text), `fixed_amount_discount`(text), `required`(bool)

---

### slideshow-hero
**Tipo:** `slideshow-hero`
**Uso:** Hero com múltiplos slides (full-screen ou altura customizada).
**Settings principais:**
- `min_desktop_height_type`, `desktop_pixels_height`
- `transparent_header`, etc.
- `slider_type`, `autoplay`, `autoplay_speed`, `enable_dots`
- `padding_top`, `padding_bottom`

**Block Types:**
- `slide` — `desktop_bg_image`, `desktop_bg_video`, `desktop_overlay_color/opacity`, `mobile_bg_image`, `heading`, `title_highlight_color`, `heading_size`, `text`, buttons 1 e 2, `color_scheme`, layout settings

---

### horizontal-ticker
**Tipo:** `horizontal-ticker`
**Uso:** Ticker horizontal infinito. Ótimo para trust badges, avisos, prova social.
**Settings principais:**
- `speed`, `direction`, `stop_on_hover`
- `color_scheme`
- `mobile_text_size`, `desktop_text_size`, `italic_text`, `uppercase_text`, `bold_text`
- `mobile_padding_top/bottom`, `desktop_padding_top/bottom`

**Block Types:**
- `text` — `title`(text)
- `image` — `image`(image_picker)
- `reviews` — review card com avatar, stars, checkmark, `author_1`, `image_1`, `text_1`
- `text_with_icon` — texto com ícones Material Symbols
- `icon_with_content` — ícone + título + texto

---

### icon-bar
**Tipo:** `icon-bar`
**Uso:** Barra de ícones/features. Pode ser grid ou slider.
**Settings principais:**
- `title`, `text`, `color_scheme`, `cards_color_scheme`
- `icon_layout`, `icon_size`, `icon_color`
- `columns_desktop`, `type`(grid/slider), `autoplay`
- `padding_top`, `padding_bottom`

**Block Types:**
- `column` — `icon`(text=Material Symbol), `filled_icon`(bool), `image`(image_picker), `title`(text), `text`(richtext)

---

### logo-list
**Tipo:** `logo-list`
**Uso:** Lista de logos ("como visto em", parceiros, etc.)
**Settings principais:**
- `title`, `gray_logos`(bool), `color_scheme`
- `layout`, `desktop_logo_height`, `mobile_logo_height`
- `columns_mobile`, `mobile_slider`, `autoplay`
- `padding_top`, `padding_bottom`

**Block Types:**
- `logo` — `image`(image_picker), `link`(url), `target_blank`(bool)

---

### video
**Tipo:** `video`
**Uso:** Seção de vídeo com cover image.
**Settings principais:**
- `title`, `heading_size`, `cover_image`(image_picker)
- `video_url`(video_url), `description`(text)
- `full_width`(bool), `color_scheme`
- `padding_top`, `padding_bottom`
**Blocks:** Nenhum

---

### image-slider
**Tipo:** `image-slider`
**Uso:** Slider de imagens ou vídeos.
**Settings principais:**
- `title`, `color_scheme`
- `type`(loop/rewind/drag), `drag`, `autoplay`, `center_mode`
- `slides_desktop`, `desktop_spacing`, `desktop_side_padding`
- `slides_mobile`, `mobile_spacing`
- `desktop_border_radius`, `mobile_border_radius`
- `padding_top`, `padding_bottom`

**Block Types:**
- `image_slide` — `image`(image_picker), `link`(url), `description`(richtext), `desc_alignment`, `desc_color_scheme`
- `video_slide` — `video`(video), `thumbnail`(image_picker), `loop`, `muted_autoplay`, `display_play_btn`, `btn_color_scheme`, `display_sound_btn`, `display_timeline`, `description`

---

### facebook-testimonials
**Tipo:** `facebook-testimonials`
**Uso:** Depoimentos com estilo de post do Facebook.
**Settings principais:**
- `title`, `text`, `color_scheme`
- `columns_desktop`, `type`(grid/slider), `autoplay`
- `post_bg_color`, `post_text_color`, `comments_bg_color`, `post_border_color`
- `like_label`, `comment_label`, `reply_label`, `share_label`
- `padding_top`, `padding_bottom`

**Block Types:**
- `column` — `post_author`, `post_author_avatar`(image_picker), `post_author_verified`, `post_time`, `post_text`(richtext), `post_image`(image_picker), `post_reactions`, `comment_1_author`, `comment_1_text`, `comment_2_author`, `comment_2_text`

---

### comparison-slider
**Tipo:** `comparison-slider`
**Uso:** Slider antes/depois (before & after) com imagens.
**Settings principais:**
- `title`, `text`, `button_label`, `color_scheme`, `layout`
- `before_label`, `after_label`, `labels_color_scheme`
- `line_color`, `arrows_style`
- `before_image`(image_picker), `after_image`(image_picker)
- `padding_top`, `padding_bottom`
**Blocks:** Nenhum (imagens configuradas nos settings)

---

### content-tabs
**Tipo:** `content-tabs`
(já descrito acima)

---

### custom-columns
**Tipo:** `custom-columns`
**Uso:** Layout de colunas totalmente customizável (1-6 colunas com widths independentes).
**Settings principais:**
- `columns_count`: 1-6
- `col_N_desktop_width`, `col_N_mobile_width`, `col_N_visibility` (para N=1 a 6)
- `column_gap_desktop`, `row_gap_desktop`, `desktop_vertical_alignment`
- `color_scheme` (aceita "custom")
- `padding_top`, `padding_bottom`

**Block Types:** heading, richtext, rating_stars, trustpilot_stars, buttons, add_to_cart_button, text_with_icon, icon_with_content, image, video, collapsible_row, email_signup, custom_liquid — cada bloco tem setting de coluna de destino

---

### vertical-ticker
**Tipo:** `vertical-ticker`
**Uso:** Ticker vertical com conteúdo lateral (split layout).
**Settings principais:**
- `number_of_rows`, `speed`, `text_size`, `ticker_color_scheme`
- `layout`, `display_content`
- Lado do conteúdo: `content_heading`, `content_text`, `button_label`, `content_color_scheme`
- `padding_top`, `padding_bottom`

**Block Types:**
- `text` — `title`(text)

---

### custom-liquid
**Tipo:** `custom-liquid`
**Uso:** Código Liquid customizado.
**Settings:** `custom_liquid`(liquid), `color_scheme`, `padding_top`, `padding_bottom`

---

### related-products
**Tipo:** `related-products`
**Uso:** Produtos relacionados (automático pelo Shopify).
**Settings:** `title`, `title_highlight_color`, `heading_size`, `products_to_show`, `columns_desktop`, `color_scheme`, `image_ratio`, `show_secondary_image`, `show_vendor`, `show_rating`, `enable_quick_add`, `columns_mobile`, `padding_top`, `padding_bottom`
**Blocks:** Nenhum

---

## TEMPLATE JSON — ESTRUTURA BÁSICA

```json
{
  "sections": {
    "ID_DA_SECAO": {
      "type": "nome-do-arquivo-sem-liquid",
      "blocks": {
        "ID_DO_BLOCO": {
          "type": "tipo_do_bloco",
          "settings": { ... }
        }
      },
      "block_order": ["ID_DO_BLOCO"],
      "settings": { ... }
    }
  },
  "order": ["ID_DA_SECAO"]
}
```

**Regras:**
- `type` da seção = nome do arquivo `.liquid` sem extensão
- IDs das seções e blocos = string alfanumérica única (ex: `main`, `hero_Ax3p`, `btn_Lm7w`)
- `block_order` deve listar todos os IDs de blocos na ordem correta
- `order` deve listar todos os IDs de seções na ordem da página
- Campos `image_picker` devem ser `""` (string vazia) se não há imagem — nunca `null`
- Campos `color_scheme: "custom"` requerem os `custom_colors_*` correspondentes
