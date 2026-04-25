import re

with open('screens/cart.html', encoding='utf-8') as f:
    cart = f.read()

# 1. Remove dollar icon from "Your profit"
cart = cart.replace(
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 2v20M17 7H9a3 3 0 100 6h6a3 3 0 110 6H7" stroke="#0C831F" stroke-width="2" stroke-linecap="round"/></svg>\n          <div class="text-[13px] font-semibold text-[#0C831F]">Your profit on this order:',
    '<div class="text-[13px] font-semibold text-[#0C831F]">Your profit on this order:'
)

# 2. VIEW ALL opens coupon sheet
old_viewall = '            <button class="text-[12px] font-semibold text-[#0E7A4E] flex items-center gap-0.5">VIEW ALL\n              <svg width="10" height="10" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="#0E7A4E" stroke-width="2.5" stroke-linecap="round"/></svg>\n            </button>'
new_viewall = '            <button onclick="openCouponSheet()" class="text-[12px] font-bold text-[#0E7A4E] flex items-center gap-0.5 bg-[#F0FDF5] px-2 py-1 rounded-lg">View All\n              <svg width="10" height="10" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="#0E7A4E" stroke-width="2.5" stroke-linecap="round"/></svg>\n            </button>'
cart = cart.replace(old_viewall, new_viewall)
print("viewall:", old_viewall in open('screens/cart.html', encoding='utf-8').read(), "->", new_viewall not in open('screens/cart.html', encoding='utf-8').read())

# 3. Improved coupon input section
old_inp = '          <div class="flex items-center gap-2 mt-2.5">\n            <input type="text" placeholder="Enter code" class="flex-1 text-[14px] text-[#1C1C1C] border border-[#EDEDED] rounded-lg px-3 py-2.5 focus:outline-none focus:border-[#0C831F] uppercase tracking-wider placeholder:normal-case placeholder:tracking-normal placeholder:text-[#9E9E9E] placeholder:font-normal">\n            <button class="bg-[#0C831F] text-white text-[13px] font-bold uppercase tracking-wider px-4 py-2.5 rounded-lg">Apply</button>\n          </div>'
new_inp = '          <div class="flex items-center gap-2 mt-2.5 p-1.5 rounded-xl" style="background:linear-gradient(135deg,#F0FDF5,#E4F5EC);border:1.5px solid rgba(14,122,78,0.25)">\n            <input type="text" id="couponInput" placeholder="Enter coupon code" class="flex-1 text-[14px] text-[#1C1C1C] bg-transparent px-2 py-1.5 focus:outline-none uppercase tracking-wider placeholder:normal-case placeholder:tracking-normal placeholder:text-[#9E9E9E] placeholder:font-normal placeholder:text-[13px]">\n            <button class="bg-[#0C831F] text-white text-[13px] font-bold uppercase tracking-wider px-4 py-2 rounded-lg flex-shrink-0">Apply</button>\n          </div>'
cart = cart.replace(old_inp, new_inp)

# 4. Upgrade distributor unlock strip
old_strip = '      <!-- Distributor unlock strip -->\n      <div class="bg-[#FFF8E6] border-b border-[#D4A537]/30 px-4 py-2">'
new_strip = '      <!-- Distributor unlock strip (matches PDP style) -->\n      <div class="px-4 py-2.5 border-b" style="background:linear-gradient(135deg,#FFFBEB,#FFF5D1);border-color:rgba(212,165,55,0.3)">'
cart = cart.replace(old_strip, new_strip)

old_lock_row = '          <div class="flex items-center gap-1.5">\n            <svg width="12" height="12" viewBox="0 0 24 24" fill="none"><rect x="5" y="11" width="14" height="10" rx="2" stroke="#8B6914" stroke-width="2"/><path d="M8 11V7a4 4 0 018-1" stroke="#8B6914" stroke-width="2"/></svg>\n            <span class="text-[12px] font-semibold text-[#8B6914]">Add <span class="font-black">&#x20B9;822</span> more to unlock distributor pricing</span>\n          </div>'
new_lock_row = '          <div class="flex items-center gap-1.5">\n            <div class="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0" style="background:rgba(212,165,55,0.2)">\n              <svg width="11" height="11" viewBox="0 0 24 24" fill="none"><rect x="5" y="11" width="14" height="10" rx="2" stroke="#8B6914" stroke-width="2.2"/><path d="M8 11V7a4 4 0 018 0v4" stroke="#8B6914" stroke-width="2.2"/></svg>\n            </div>\n            <span class="text-[12px] font-semibold text-[#8B6914]">Add <span class="font-black text-[#1C1C1C]">&#x20B9;822</span> more → unlock Distributor price</span>\n          </div>'
cart = cart.replace(old_lock_row, new_lock_row)

old_bar = '        <div class="h-1 bg-white border border-[#D4A537]/25 rounded-full overflow-hidden">\n          <div class="h-full rounded-full" style="width:62%;background:linear-gradient(90deg,#D4A537,#8B6914)"></div>\n        </div>'
new_bar = '        <div class="h-1.5 bg-white/60 border border-[#D4A537]/20 rounded-full overflow-hidden">\n          <div class="h-full rounded-full" style="width:62%;background:linear-gradient(90deg,#D4A537,#FFB900,#8B6914)"></div>\n        </div>\n        <div class="flex justify-between mt-1 text-[9px] text-[#B45309]"><span>₹1,430 in cart</span><span>₹2,252 needed to unlock</span></div>'
cart = cart.replace(old_bar, new_bar)

# 5. Add coupon sheet HTML + JS before service worker script
coupon_html = '''
  <!-- Coupon sheet -->
  <div id="couponSheetBd" class="hidden absolute inset-0 bg-black/45 z-40" onclick="closeCouponSheet()"></div>
  <div id="couponSheet" class="hidden absolute left-0 right-0 bottom-0 z-50 bg-white rounded-t-[28px]" style="box-shadow:0 -8px 30px rgba(0,0,0,.15);max-height:75%;overflow-y:auto">
    <div class="px-5 pt-2.5 pb-6">
      <div class="mx-auto w-10 h-1 rounded-full bg-[#E8E8E8] mb-4"></div>
      <div class="flex items-center justify-between mb-4">
        <div class="brand-font text-[20px] text-[#1C1C1C]">3 Offers Available</div>
        <button onclick="closeCouponSheet()" class="text-[13px] font-medium text-[#606060] border border-[#EDEDED] rounded-full px-3 py-1">Close</button>
      </div>
      <div class="space-y-3">
        <div class="border border-dashed border-[#D4A537] rounded-2xl p-3.5" style="background:linear-gradient(135deg,#FFFDF5,#FFF8E6)">
          <div class="flex items-start justify-between gap-2 mb-1">
            <div><div class="text-[14px] font-black text-[#1C1C1C]">FARMER10</div><div class="text-[12px] text-[#8B6914] mt-0.5">10% off up to &#8377;100 &middot; best for this cart</div></div>
            <button onclick="applyCoupon('FARMER10')" class="text-[13px] font-black text-[#0C831F] uppercase bg-[#F0FDF5] border border-[#0C831F]/30 px-3 py-2 rounded-xl whitespace-nowrap">Apply</button>
          </div>
          <div class="text-[11px] text-[#606060] pt-2 border-t border-[#D4A537]/20">Min. cart &#8377;500 &middot; Valid till 30 Apr</div>
        </div>
        <div class="border border-dashed border-[#0E7A4E]/40 rounded-2xl p-3.5" style="background:linear-gradient(135deg,#F8FFFC,#F0FDF5)">
          <div class="flex items-start justify-between gap-2 mb-1">
            <div><div class="text-[14px] font-black text-[#1C1C1C]">FIRSTORDER</div><div class="text-[12px] text-[#0E7A4E] mt-0.5">Flat &#8377;200 off on first order above &#8377;2,000</div></div>
            <button onclick="applyCoupon('FIRSTORDER')" class="text-[13px] font-black text-[#0C831F] uppercase bg-[#F0FDF5] border border-[#0C831F]/30 px-3 py-2 rounded-xl whitespace-nowrap">Apply</button>
          </div>
          <div class="text-[11px] text-[#606060] pt-2 border-t border-[#0E7A4E]/15">New partners only &middot; expires in 5 days</div>
        </div>
        <div class="border border-dashed border-[#EDEDED] rounded-2xl p-3.5" style="background:#FAFAFA">
          <div class="flex items-start justify-between gap-2 mb-1">
            <div><div class="text-[14px] font-black text-[#1C1C1C]">KHARIF5</div><div class="text-[12px] text-[#606060] mt-0.5">5% off on pesticides above &#8377;3,000</div></div>
            <button onclick="applyCoupon('KHARIF5')" class="text-[13px] font-black text-[#606060] uppercase bg-white border border-[#EDEDED] px-3 py-2 rounded-xl whitespace-nowrap">Apply</button>
          </div>
          <div class="text-[11px] text-[#9E9E9E] pt-2 border-t border-[#EDEDED]">Min. &#8377;3,000 &middot; Pesticides only</div>
        </div>
      </div>
    </div>
  </div>
  <script>
  function openCouponSheet(){document.getElementById('couponSheetBd').classList.remove('hidden');document.getElementById('couponSheet').classList.remove('hidden');}
  function closeCouponSheet(){document.getElementById('couponSheetBd').classList.add('hidden');document.getElementById('couponSheet').classList.add('hidden');}
  function applyCoupon(c){var i=document.getElementById('couponInput');if(i)i.value=c;closeCouponSheet();}
  </script>
'''
cart = cart.replace('  <script>if("serviceWorker"in navigator)', coupon_html + '  <script>if("serviceWorker"in navigator)')

with open('screens/cart.html', 'w', encoding='utf-8') as f:
    f.write(cart)
print("cart.html done")
