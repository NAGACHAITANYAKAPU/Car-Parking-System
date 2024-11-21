from flask import render_template, request, redirect, url_for, session, flash
from app import app
from app.models.supervisor import Supervisor
from app.models.user import User 
from .decorators import login_required
import logging
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from app.models.feedback import Feedback
from app.models.payment import Payment
from app.models.space import Pspace
from flask import jsonify



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/admin_view_pending_spaces')
@login_required
def admin_view_pending_spaces():
    pending_spaces = Pspace.find({"status": "pending"})
    return render_template('admin/view_pending_spaces.html', pending_spaces=pending_spaces)

@app.route('/admin_view_space_detail')
@login_required
def admin_view_space_detail():
     
    pass

@app.route('/admin_accept_space/<space_id>', methods=['POST'])
@login_required
def admin_accept_space(space_id):
    # Update the parking space status to 'active'
    Pspace.update_one({"_id": ObjectId(space_id)}, {"$set": {"status": "active"}})
    flash("Parking space accepted and activated.", "success")
    return redirect(url_for('admin_view_pending_spaces'))

@app.route('/admin_reject_space/<space_id>', methods=['POST'])
@login_required
def admin_reject_space(space_id):
    # Update the parking space status to 'rejected'
    Pspace.update_one({"_id": ObjectId(space_id)}, {"$set": {"status": "rejected"}}) 
    return redirect(url_for('admin_view_pending_spaces'))
